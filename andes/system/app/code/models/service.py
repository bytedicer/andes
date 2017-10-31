from db import db

class ServiceModel(db.Model):
  __tablename__ = 'services'

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(32))
  image = db.Column(db.String(64))
  exposed_ports = db.Column(db.String(255))
  volumes = db.Column(db.String(1024))

  # TODO: make volumes optional
  def __init__(self, name, image, exposed_ports, volumes):
    self.name = name
    self.image = image
    self.exposed_ports = exposed_ports
    self.volumes = volumes

  def json(self):
    return {
      'id': self.id,
      'name': self.name,
      'image': self.image,
      'exposed_ports': self.exposed_ports.split(','),
      'volumes': self.volumes.split(',')
    }

  # TODO: Test those functions
  # TODO: validate if image exists

  @classmethod
  def valid_volumes(cls, volume_string):
    try:
      for volume in volume_string.split(','):
        if not volume.startswith('/'):
          return False
    except:
      return False

    return True

  @classmethod
  def valid_ports(cls, port_string):
    try:
      for port in port_string.split(','):
        port = int(port)
        if port < 0 or port > 65535:
          return False
    except:
      return False

    return True

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
