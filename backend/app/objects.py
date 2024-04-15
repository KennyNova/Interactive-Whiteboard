from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

class Shape(Enum):
    LINE = 'line'
    CIRCLE = 'circle'
    RECT = 'rect'
    IMAGE = 'image'

class CtxMode(Enum):
    ERASER = 'eraser'
    DRAW = 'draw'
    SELECT = 'select'

@dataclass
class RgbaColor:
    r: int
    g: int
    b: int
    a: float

@dataclass
class Selection:
    x: int
    y: int
    width: int
    height: int

@dataclass
class CtxOptions:
    lineWidth: int
    lineColor: RgbaColor
    fillColor: RgbaColor
    shape: Shape
    mode: CtxMode
    selection: Optional[Selection] = None

@dataclass
class Circle:
    cX: int
    cY: int
    radiusX: int
    radiusY: int

@dataclass
class Rect:
    width: int
    height: int

@dataclass
class Img:
    base64: str

@dataclass
class Move:
    circle: Circle
    rect: Rect
    img: Img
    path: List[Tuple[int, int]]
    options: CtxOptions
    timestamp: int
    id: str
    roomId: str

class Room:
    usersMoves: Dict[str, List[Move]]
    drawed: List[Move]
    users: Dict[str, str]

@dataclass
class User:
    name: str
    color: str

class ClientRoom:
    id: str
    usersMoves: Dict[str, List[Move]]
    movesWithoutUser: List[Move]
    myMoves: List[Move]
    users: Dict[str, User]

@dataclass
class MessageType:
    userId: str
    username: str
    color: str
    msg: str
    id: int

class ServerToClientEvents:
    def room_exists(self, exists: bool) -> None:
        pass

    def joined(self, roomId: str, failed: Optional[bool] = None) -> None:
        pass

    def room(self, room: Room, usersMovesToParse: str, usersToParse: str) -> None:
        pass

    def created(self, roomId: str) -> None:
        pass

    def your_move(self, move: Move) -> None:
        pass

    def user_draw(self, move: Move, userId: str) -> None:
        pass

    def user_undo(self, userId: str) -> None:
        pass

    def mouse_moved(self, x: int, y: int, userId: str) -> None:
        pass

    def new_user(self, userId: str, username: str) -> None:
        pass

    def user_disconnected(self, userId: str) -> None:
        pass

    def new_msg(self, userId: str, msg: str) -> None:
        pass

class ClientToServerEvents:
    def check_room(self, roomId: str) -> None:
        pass

    def draw(self, move: Move) -> None:
        pass

    def mouse_move(self, mousePos: dict) -> None:
        pass

    def undo(self) -> None:
        pass

    def create_room(self, data: dict) -> None:
        pass

    def join_room(self, data: dict) -> None:
        pass

    def joined_room(self) -> None:
        pass

    def leave_room(self) -> None:
        pass

    def send_msg(self, msg: str) -> None:
        pass
