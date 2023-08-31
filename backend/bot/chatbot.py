import json
from pickle import NONE
import aux.constants as Constants
import logging 
import requests
from bot.connection_manager import manager
from flightbooking.AviationStackHandler import aviationStackHandler
from sql_app.schemas import booking as BookingSchemas, feedback as FeedbackSchemas
from sql_app.crud import crud_booking, crud_feedback
from sqlalchemy.orm import Session

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

class ChatBot:


    async def send(self,db: Session, sender, message):
        
        msg_type = message['content_type']
        text = message['content']
        logging.info("HEYYYYY")
        logging.info(message)
        response = self.check_user_msg_type(db,sender,msg_type, text)
        if response:
            msg_type = Constants.MESSAGE_TYPE_TEXT
            await manager.send_message(sender, msg_type, response)
            return

        data = { 'sender': sender, 'message': text }
        r = requests.post(Constants.CHATBOT_HOST, json=data,
            verify=False)
        res = r.json()[0]

        client_id, message, msg_type = int(res['recipient_id']), res['custom'], res['custom']['msg_type']
        response, msg_type = self.check_bot_msg_type(db, client_id, msg_type, message)
        logging.info(client_id)
        logging.info(message)
        logging.info(msg_type)
        await manager.send_message(client_id, msg_type, response)


    def check_user_msg_type(self, db: Session, sender, msg_type, text):
        if msg_type == Constants.MESSAGE_TYPE_BOOKING:
            text = json.loads(text)

            booking_data= BookingSchemas.BookingCreate(
                    user=int(sender),
                    flight_icao=text['flight_icao'],
                    price=text['price'],
                    flight_number=text['flight_number'],
                    departure_time=text['departure_time']
                    )
            crud_booking.create_booking(db,booking_data)
            logging.info("Booking created")
            return "Your Booking has been sucessfully created!"
        
        elif msg_type == Constants.MESSAGE_TYPE_FEEDBACK:
            feedback = FeedbackSchemas.FeedBackCreate(
                user_id=sender,
                rating =int(text[-1]
                )
            )
            logging.info(text)
            crud_feedback.create_feedback(
                db=db,
                feedback_data=feedback
            )
            logging.info(f"Added Review from user with id {sender}")
            return "Thank you for your feedback."

        elif msg_type == Constants.MESSAGE_TYPE_HELP_REQUEST:
            manager.update_status(sender,Constants.HELP_REQUEST_STATUS)
        
        elif msg_type == Constants.MESSAGE_TYPE_HELP_REQUEST_ACCEPTED:
            manager.update_receiver(sender,int(text['manager_id']) )
        
        elif msg_type == Constants.MESSAGE_TYPE_HELP_REQUEST_FINISHED:
            manager.update_status(sender,Constants.NORMAL_STATUS)
            manager.update_receiver(sender, None)

        return None


    def check_bot_msg_type(self,db: Session, sender, msg_type, message):
        data = None
        if msg_type == Constants.MESSAGE_TYPE_SEARCH:
            city_departure = message['city_departure']
            city_arrival = message['city_arrival']
            user_budget = float(message['budget'])
            data = aviationStackHandler.get_availableFlights(city_departure,
            city_arrival, user_budget)
            print(data)
            if not data:
                return f"No flights available from {city_departure} to {city_arrival}", 'text'

        elif msg_type == Constants.MESSAGE_TYPE_CHECKBOOKING:
            logging.info(f"Retrieved User {sender} bookings")
            #data = crud_booking.get_bookingsByUserId(db,userId=sender)
            data = "Checking for your booked flights..."
        else:
            data = message['text']
            
        return data, msg_type


            

        


chatbotclient = ChatBot()