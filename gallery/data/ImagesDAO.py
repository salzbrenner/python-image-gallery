from .BaseDAO import BaseDAO
from .Image import Image


class ImagesDAO(BaseDAO):
    def get_images(self, username):
        res = self.execute("""select * from 
                                images img 
                                where img.username = %s;
                                """,
                           (username,))
        images = []
        for row in res:
            images.append(Image(row[0], row[1], row[2]))
        return images

    def get_single_image(self, username=None, filename=None, image_id=None):

        if image_id:
            res = self.execute("""select * from 
                                       images img 
                                       where img.id = %s
                                       """,
                               (image_id))
        else:
            res = self.execute("""select * from 
                                        images img 
                                        where img.username = %s
                                        and img.filename = %s;
                                        """,
                               (username, filename))

        if res.rowcount == 0:
            return None

        for row in res:
            return Image(row[0], row[1], row[2])

    def delete_image(self, username, filename):
        self.execute("""delete from 
                        images img 
                        where img.username = %s
                        and img.filename = %s;
                    """,
                     (username, filename))

        self.save()
        return True

    def add_image(self, username, filename):
        if not any(d['filename'] == filename for d in self.get_images(username)):
            self.execute("insert into images values (DEFAULT, %s, %s);",
                         (username, filename))
            self.save()
            return True
        return False
