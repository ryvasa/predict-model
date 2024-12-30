import pika
import joblib
import json
import numpy as np
import sys
import os

# Load model
model = joblib.load('src/xgboost_model.pkl')

# Fungsi untuk memprediksi harga
def predict_price(data):
    input_data = np.array([[
        data['area'],
        data['harvest_time'],
        data['harvest_yield'],
        data['demand'],
        data['supply'],
        data['sale'],
        data['day']
    ]])
    try:
        prediction = model.predict(input_data)[0]
        return float(prediction)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel_in = connection.channel()
    channel_out = connection.channel()

    # Deklarasi antrian input dan output
    channel_in.queue_declare(queue='prediction-input-queue')
    channel_out.queue_declare(queue='prediction-output-queue')


    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            print(data)
            predicted_price = predict_price(data)
            if predicted_price is not None:
                result = {'original_data': data, 'predicted_price': predicted_price}
                channel_out.basic_publish(exchange='',
                                          routing_key='prediction-output-queue',
                                          body=json.dumps(result))
                print(f" [x] Predicted price: {predicted_price}, Sent to output queue.")
            else:
                print("Prediction failed. Message dropped.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")


    channel_in.basic_consume(queue='prediction-input-queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel_in.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
