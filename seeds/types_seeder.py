from datetime import date, datetime
from flask_seeder import Seeder, Faker, generator
from core.models.message_type import MessageType


class MessageTypeSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    def run(self):

        media_type1 =  MessageType(t_name="Upload MP4 Video",t_description = "Upload MP4 Video", created_at = datetime.now())
        media_type2 =  MessageType(t_name="Mp4 video link",t_description = "mp4 video link", created_at = datetime.now())
        media_type3 =  MessageType(t_name="Youtube video link",t_description = "Youtube video link", created_at = datetime.now())
        media_type4 =  MessageType(t_name="Vimeo video link",t_description = "Vimeo video link", created_at = datetime.now())
        media_type5 =  MessageType(t_name="Dailymotion video link",t_description = "Dailymotion video link", created_at = datetime.now())
        media_type6 =  MessageType(t_name="Mpd video link",t_description = "mpd video link", created_at = datetime.now())
        media_type7 =  MessageType(t_name="m3u8 video Link",t_description = "m3u8 video Link", created_at = datetime.now())

        self.db.session.add_all([media_type1, media_type2, media_type3, media_type4,media_type5, media_type6, media_type7])
        self.db.session.commit()