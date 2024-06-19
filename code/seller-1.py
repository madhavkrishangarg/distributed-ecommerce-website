import grpc
import uuid
import logging
import market_pb2
import market_pb2_grpc
from concurrent import futures
import threading

seller_uuid = str(uuid.uuid1())

class Seller(market_pb2_grpc.MarketplaceServicer):
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = market_pb2_grpc.MarketplaceStub(self.channel)
        self.seller_uuid = seller_uuid
        self.seller_address = "localhost:50052"
        # self.registerSeller()
        
    def registerSeller(self):
        response = self.stub.registerSeller(market_pb2.registerSellerRequest(uuid=self.seller_uuid, address=self.seller_address))
        print(response)
        if response.success:
            print(f"Registered as seller with uuid={self.seller_uuid}")
        else:
            print(f"Failed to register as seller with uuid={self.seller_uuid}")
            
    def sellItem(self, name, category, quantity, description, price):
        if(category == "electronics"):
            print(category)
            response = self.stub.sellItem(market_pb2.sellItemRequest(name=name, electronics=True, quantity=quantity, description=description, seller_uuid=self.seller_uuid, seller_address=self.seller_address, price=price))
        elif(category == "fashion"):
            print(category)
            response = self.stub.sellItem(market_pb2.sellItemRequest(name=name, fashion=True, quantity=quantity, description=description, seller_uuid=self.seller_uuid, seller_address=self.seller_address, price=price))
        else:
            response = self.stub.sellItem(market_pb2.sellItemRequest(name=name, other=True, quantity=quantity, description=description, seller_uuid=self.seller_uuid, seller_address=self.seller_address, price=price))
        
        if response.success:
            print(f"Item {name} with uuid={response.item_id} added to the market")
        else:
            print(f"Failed to add item {name} to the market")
            
    def updateItem(self, item_uuid, price=None, quantity=None, description=None):
        response = self.stub.updateItem(market_pb2.updateItemRequest(item_id=item_uuid, price=price, quantity=quantity, description=description, seller_uuid=self.seller_uuid, seller_address=self.seller_address))
        
        if response.success:
            print(f"Item with uuid={item_uuid} updated successfully")
        else:
            print(f"Failed to update item with uuid={item_uuid}")
            
    def deleteItem(self, item_uuid):
        response = self.stub.deleteItem(market_pb2.deleteItemRequest(item_id=item_uuid, seller_uuid=self.seller_uuid, seller_address=self.seller_address))
        
        if response.success:
            print(f"Item with uuid={item_uuid} deleted successfully")
        else:
            print(f"Failed to delete item with uuid={item_uuid}")
            
    def displaySellerItems(self):
        try:
            response_iterator = self.stub.displaySellerItems(market_pb2.displaySellerItemsRequest(seller_uuid=self.seller_uuid, seller_address=self.seller_address))
            print("Items listed by the seller:")
            for item in response_iterator:
                category = "electronics" if item.electronics else ("fashion" if item.fashion else "other")
                # print(item.__str__())
                print(f"Item id: {item.item_id}, Name: {item.name}, Category: {category}, Quantity: {item.quantity}, Description: {item.description}, Seller UUID: {item.seller_uuid}, Price: {item.price}, Rating: {item.rating}")
        except Exception as e:
            print("error: ", e)
        #problem with oneof

    def notifySeller(self, request, context):
        try:
            print(f"\nReceived notification: {request.msg}\n")
            return market_pb2.notifySellerResponse(success=True)
        except:
            return market_pb2.notifySellerResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketplaceServicer_to_server(Seller(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    seller = Seller()
    seller.registerSeller()
    server_thread = threading.Thread(target=serve)
    server_thread.start()
    
    while True:
        print("1. Sell item")
        print("2. Update item")
        print("3. Delete item")
        print("4. Display seller items")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            name = input("Enter item name: ")
            category = input("Enter item category (electronics/fashion/other): ")
            quantity = int(input("Enter item quantity: "))
            description = input("Enter item description: ")
            price = int(input("Enter item price: "))
            seller.sellItem(name, category, quantity, description, price)
        
        elif choice == 2:
            item_uuid = int(input("Enter item uuid: "))
            price = input("Enter new price: ")
            if(price):
                price = int(price)
            else:
                price = None
                
            quantity = input("Enter new quantity: ")
            if(quantity):
                quantity = int(quantity)
            else:
                quantity = None
                
            description = input("Enter new description: ")
            if(description == ""):
                description = None
                
            seller.updateItem(item_uuid, price, quantity, description)
        
        elif choice == 3:
            item_uuid = int(input("Enter item uuid: "))
            seller.deleteItem(item_uuid)
            
        elif choice == 4:
            seller.displaySellerItems()
    
        else:
            break