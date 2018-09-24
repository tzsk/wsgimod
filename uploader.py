import os
from exceptions import FileUploaderError, FileOverwriteError, UploadedFileSaveError, MoveDestinationError, MoveError

class FileUploader(object):
	"""
	FileUploader object provides basic functionality to
	work with files uploaded with wsgimod.HttpRequest object
	
	Naturally there is no need to instantiate it as far as it is
	instantiated automatically by HttpRequest during the HTTP
	request processing.
	
	It is enough to use it as:
	::
		import wsgimod
		
		def my_wsgi_app( environ, start_response):
			status = '200 OK'
			response_headers = [('Content-type','text/plain')]
			start_response( status, response_headers)
			
			request = wsgimod.HttpRequest( environ)
			
			if request.has_files():
				try :
					request.FileUploader.move_all(
						destination = '/my/cool/file/storage',
						overwrite = True
					)
					my_response = 'Thank you, we saved all you pass!'
				
				except FileUploaderError as e:
					my_response = "Oops, we can't save this! Reason: %s" %e
			
			else :
				my_response = 'There is nothing to do, sorry...'
			
			return my_response
	"""

	def __init__(self, files, tmp_dir):
		self.FILES      = files
		self.tmp_dir    = tmp_dir
	
	def move(self, file, destination, overwrite = False):
		"""
		Moves a single uploaded file from a temporary location to the
		given destination. If overwrite is turned on file will be
		overwritten during the move, otherwise error will be raised
		
		:param file: dict - file description compatible by structure with the \
		FILES storage item from wsgimod.HttpRequest
		:param destination: str - path where to move the file. If existing directory \
		provided will save the file in that directory with the file name \
		passed in HTTP request
		:param overwrite: bool - flag, to turn on/off files overwriting
		:rtype: returns new file destination on success
		:raise: FileOverwriteError, UploadedFileSaveError or MoveError
		"""
		if type(file) is dict and 'tmp_name' in file:
			ext = file['filename'].split('.')[-1]
			if os.path.isdir( destination):
				destination += '/' + file['tmp_name'] + '.' + ext
			
			if os.path.isfile( destination) and not overwrite:
				raise FileOverwriteError( destination)
			
			try :
				os.rename( self.tmp_dir + '/' + file['tmp_name'], destination)
				return destination
			except Exception as e:
				raise UploadedFileSaveError( destination, e)
		else:
			raise MoveError()
	
	def move_all(self, destination, overwrite = False, fdict = None):
		"""
		Moves all the files uploaded during HTTP request to the given destination
		
		:param destination: str - path where to store the files. Destination MUST \
		be a directory, otherwise an error will be raised
		:param overwrite: bool - flag, to turn on/off files overwriting
		:rtype: list - new files destinations
		:raise: FileOverwriteError, UploadedFileSaveError, MoveDestinationError or MoveError
		"""
		moved_files = []
		
		if not os.path.isdir( destination):
			raise MoveDestinationError( destination)
		
		if fdict is None:
			fdict = self.FILES
		
		for file in fdict.values():
			if type(file) is dict and 'tmp_name' not in file:
				moved_files += self.move_all( destination, overwrite, file)
			
			elif 'tmp_name' in file:
				moved_files += [self.move( file, destination, overwrite)]
			
			else:
				raise MoveError()
		
		return moved_files