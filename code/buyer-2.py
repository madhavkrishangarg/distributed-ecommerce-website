import grpc
import uuid
import logging
import market_pb2
import market_pb2_grpc
from concurrent import futures
import threading

buyer_uuid = str(uuid.uuid1())

class Buyer(market_pb2_grpc.MarketplaceServicer):
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = market_pb2_grpc.MarketplaceStub(self.channel)
        self.buyer_uuid = buyer_uuid
        self.buyer_address = "localhost:50055"
        
    def searchItem(self, name=None, category=None):
        if category == "electronics":
            response = self.stub.searchItem(market_pb2.searchItemRequest(name=name, electronics=True))
        elif category == "fashion":
            response = self.stub.searchItem(market_pb2.searchItemRequest(name=name, fashion=True))
        elif category == "other":
            response = self.stub.searchItem(market_pb2.searchItemRequest(name=name, other=True))
        else:
            response = self.stub.searchItem(market_pb2.searchItemRequest(name=name, other=False))

        for item in response:
            if item.item_id:
                category = "electronics" if item.electronics else ("fashion" if item.fashion else "other")
                print(f"Item id: {item.item_id}, Name: {item.name}, Category: {category}, Quantity: {item.quantity}, Description: {item.description}, Seller UUID: {item.seller_uuid}, Price: {item.price}, Rating: {item.rating}")
            else:
                print("No items found")

         
    def buyItem(self, item_id, quantity):
        response = self.stub.buyItem(market_pb2.buyItemRequest(item_id=item_id, quantity=quantity, address=self.buyer_address))
        
        if response.success:
            print(f"Item with id={item_id} bought successfully")
        else:
            print(f"Failed to buy item with id={item_id}")
        
            
    def addToWishlist(self, item_id):
        response = self.stub.addToWishlist(market_pb2.addToWishlistRequest(item_id=item_id, address=self.buyer_address))
        if response.success:
            print(f"Item with id={item_id} added to wishlist successfully")
        else:
            print(f"Failed to add item with id={item_id} to wishlist")
            
    def rateItem(self, item_id, rating):
        response = self.stub.rateItem(market_pb2.rateItemRequest(item_id=item_id, rating=rating, address=self.buyer_address))
        if(response.success):
            print(f"Item with id={item_id} rated successfully")
        else:
            print(f"Failed to rate item with id={item_id}")
        
    def notifyBuyer(self, request, context):
        try:
            print(f"\nReceived notification: {request.msg}\n")
            return market_pb2.notifyBuyerResponse(success=True)
        except:
            return market_pb2.notifyBuyerResponse(success=True)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketplaceServicer_to_server(Buyer(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    buyer = Buyer()
    server_thread = threading.Thread(target=serve)
    server_thread.start()
    
    while True:
        print("1. Search item")
        print("2. Buy item")
        print("3. Add to wishlist")
        print("4. Rate item")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            name = input("Enter item name: ")
            category = input("Enter item category (electronics/fashion/other/any): ")
            buyer.searchItem(name, category)
            
        elif choice == 2:
            item_id = int(input("Enter item id: "))
            quantity = int(input("Enter quantity: "))
            buyer.buyItem(item_id, quantity)
            
        elif choice == 3:
            item_id = int(input("Enter item id: "))
            buyer.addToWishlist(item_id)
            
        elif choice == 4:
            item_id = int(input("Enter item id: "))
            rating = int(input("Enter rating: "))
            buyer.rateItem(item_id, rating)
            
        else:
            break