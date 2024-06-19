from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ("item_id", "name", "electronics", "fashion", "other", "price", "quantity", "description", "seller_address", "seller_uuid", "rating")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELECTRONICS_FIELD_NUMBER: _ClassVar[int]
    FASHION_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    name: str
    electronics: bool
    fashion: bool
    other: bool
    price: int
    quantity: int
    description: str
    seller_address: str
    seller_uuid: str
    rating: int
    def __init__(self, item_id: _Optional[int] = ..., name: _Optional[str] = ..., electronics: bool = ..., fashion: bool = ..., other: bool = ..., price: _Optional[int] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ..., rating: _Optional[int] = ...) -> None: ...

class registerSellerRequest(_message.Message):
    __slots__ = ("address", "uuid")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    address: str
    uuid: str
    def __init__(self, address: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class registerSellerResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class sellItemRequest(_message.Message):
    __slots__ = ("name", "electronics", "fashion", "other", "quantity", "description", "seller_address", "price", "seller_uuid")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELECTRONICS_FIELD_NUMBER: _ClassVar[int]
    FASHION_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    name: str
    electronics: bool
    fashion: bool
    other: bool
    quantity: int
    description: str
    seller_address: str
    price: int
    seller_uuid: str
    def __init__(self, name: _Optional[str] = ..., electronics: bool = ..., fashion: bool = ..., other: bool = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., price: _Optional[int] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class sellItemResponse(_message.Message):
    __slots__ = ("success", "item_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    item_id: int
    def __init__(self, success: bool = ..., item_id: _Optional[int] = ...) -> None: ...

class updateItemRequest(_message.Message):
    __slots__ = ("item_id", "price", "quantity", "description", "seller_address", "seller_uuid")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    price: int
    quantity: int
    description: str
    seller_address: str
    seller_uuid: str
    def __init__(self, item_id: _Optional[int] = ..., price: _Optional[int] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., seller_uuid: _Optional[str] = ...) -> None: ...

class updateItemResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class deleteItemRequest(_message.Message):
    __slots__ = ("item_id", "seller_uuid", "seller_address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    seller_uuid: str
    seller_address: str
    def __init__(self, item_id: _Optional[int] = ..., seller_uuid: _Optional[str] = ..., seller_address: _Optional[str] = ...) -> None: ...

class deleteItemResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class displaySellerItemsRequest(_message.Message):
    __slots__ = ("seller_uuid", "seller_address")
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    seller_uuid: str
    seller_address: str
    def __init__(self, seller_uuid: _Optional[str] = ..., seller_address: _Optional[str] = ...) -> None: ...

class searchItemRequest(_message.Message):
    __slots__ = ("name", "electronics", "fashion", "other")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ELECTRONICS_FIELD_NUMBER: _ClassVar[int]
    FASHION_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    name: str
    electronics: bool
    fashion: bool
    other: bool
    def __init__(self, name: _Optional[str] = ..., electronics: bool = ..., fashion: bool = ..., other: bool = ...) -> None: ...

class buyItemRequest(_message.Message):
    __slots__ = ("item_id", "quantity", "address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    quantity: int
    address: str
    def __init__(self, item_id: _Optional[int] = ..., quantity: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class buyItemResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class addToWishlistRequest(_message.Message):
    __slots__ = ("item_id", "address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    address: str
    def __init__(self, item_id: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class addToWishlistResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class rateItemRequest(_message.Message):
    __slots__ = ("item_id", "rating", "address")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    rating: int
    address: str
    def __init__(self, item_id: _Optional[int] = ..., rating: _Optional[int] = ..., address: _Optional[str] = ...) -> None: ...

class rateItemResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class notifySellerRequest(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class notifySellerResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class notifyBuyerRequest(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class notifyBuyerResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
