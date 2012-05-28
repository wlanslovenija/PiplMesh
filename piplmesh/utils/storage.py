import uuid

from mongoengine.django import storage

class GridFSStorage(storage.GridFSStorage):
    """
    A storage backend to store files in GridFS, with
    streaming save, and UUID filenames.
    """

    def _save(self, name, content):
        if not hasattr(content, 'chunks'):
            return super(GridFSStorage, self)._save(name, content)

        doc = self.document()
        field = getattr(doc, self.field)

        field.new_file(filename=name)
        for chunk in content.chunks():
            field.write(chunk)
        field.close()

        doc.save()

        return name

    def get_available_name(self, name):
        # We ignore given name
        name = str(uuid.uuid4())

        while self.exists(name):
            name = str(uuid.uuid4())

        return name
