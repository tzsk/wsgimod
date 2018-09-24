class HttpRequestError(Exception):
	pass

class MaxFilesError(HttpRequestError):
	def __init__(self, limit):
		self.limit = limit
	
	def __str__(self):
		return "Max uploaded files limit of %i files exceeded" %(self.limit)

class MaxFileSizeError(HttpRequestError):
	def __init__(self, filename, sizelimit):
		self.filename  = filename
		self.sizelimit = sizelimit
	
	def __str__(self):
		return 'Uploaded file "%s" exceeded size limit of %i bytes' %(self.filename, self.sizelimit)

class MaxBodySizeError(HttpRequestError):
	def __init__(self, sizelimit):
		self.sizelimit  = sizelimit
	
	def __str__(self):
		return 'Max request body size limit of %i bytes exceeded' %(self.sizelimit)

class FilesUploadError(HttpRequestError):
	def __str__(self):
		return "Files upload was disabled, but files were found in request body"

class FileSaveError(HttpRequestError):
	def __init__(self, filename, path, reason = None):
		self.filename = filename
		self.path     = path
		self.reason   = reason
	
	def __str__(self):
		return 'Error saving file "%s"\n Reason: %s' %(self.filename, self.reason)


class FileUploaderError(Exception):
	pass

class FileOverwriteError(FileUploaderError):
	def __init__(self, filename):
		self.filename = filename
	
	def __str__(self):
		return 'Can not save file "%s". Such file already exists' %(self.filename)

class UploadedFileSaveError(FileUploaderError):
	def __init__(self, filename, reason):
		self.filename = filename
		self.reason = reason
	
	def __str__(self):
		return 'Can not save file "%s". Reason: %s' %(self.filename, self.reason)

class MoveError(FileUploaderError):
	def __str__(self):
		return 'Given file is invalid - expecting object from HttpRequest.FILES'

class MoveDestinationError(FileUploaderError):
	def __init__(self, destination):
		self.destination = destination
	
	def __str__(self):
		return 'Given destination "%s" is not a directory' %(self.destination)
