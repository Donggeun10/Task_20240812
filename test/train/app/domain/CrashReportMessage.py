from enum import Enum

LogVersion = Enum("LogVersion", "v1 v2 v3 v4")

class BaseMessage():

  game_code : str
  device_os : str
  log : object
  version : LogVersion

  def __init__(self, game_code : str, device_os : str, log : object, version : LogVersion):
    self.game_code = game_code
    self.device_os = device_os
    self.log = log
    self.version = version

  def __str__(self):
    return (f"BaseMessage game_code: {self.game_code}, device_os:{self.device_os}, log: {self.log}, version: {self.version}")

class InitMessage(BaseMessage):

  def __init__(self, game_code : str, device_os : str, log : object, version : LogVersion):
    super().__init__(game_code, device_os, log, version)

  def __str__(self):
    return f"InitMessage : {super().__str__()}"

class InitResponse():
  ping_hosts : list
  ping_count : int
  httpstat_urls : list
  httpstat_count : int

  def __init__(self, ping_hosts : list, ping_count : int, httpstat_urls : list, httpstat_count : int):
    self.ping_hosts = ping_hosts
    self.ping_count = ping_count
    self.httpstat_urls = httpstat_urls
    self.httpstat_count = httpstat_count

  def __str__(self):
    return (f"InitResponse pingHosts: {self.ping_hosts}, pingCount:{self.ping_count}, httpstatUrls: {self.httpstat_urls}, httpstatCount: {self.httpstat_count}")