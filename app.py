import os
from flask import Flask, render_template, jsonify, request
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('../.env')

app = Flask(__name__)

SUPABASE_URL = os.getenv('VITE_SUPABASE_URL')
SUPABASE_KEY = os.getenv('VITE_SUPABASE_ANON_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/orders/update-status', methods=['POST'])
def update_order_status():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        status = data.get('status')
        
        if not order_id or not status:
            return jsonify({'success': False, 'error': 'Missing order_id or status'}), 400
        
        # Call Supabase RPC function to update order status
        response = supabase.rpc('update_order_status', {
            'p_order_id': order_id,
            'p_status': status
        }).execute()
        
        if response.data:
            return jsonify(response.data)
        else:
            return jsonify({'success': False, 'error': 'Failed to update order status'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/orders')
def get_orders():
    try:
        response = supabase.rpc('get_order_details').execute()
        
        if response.data:
            orders = []
            for row in response.data:
                orders.append({
                    'order_id': row['order_id'],
                    'order_date': row['order_date'],
                    'total_amount': float(row['total_amount']),
                    'status': row['status'],
                    'student_name': row['student_name'],
                    'roll_number': row.get('roll_number'),
                    'phone': row.get('phone'),
                    'role': row.get('role', 'student'),
                    'branch': row['branch'],
                    'year': row['year'],
                    'items': row['items']
                })
            return jsonify({'success': True, 'orders': orders})
        else:
            return jsonify({'success': True, 'orders': []})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/orders/stats')
def get_stats():
    try:
        orders_response = supabase.table('orders').select('total_amount, created_at').execute()
        
        total_orders = len(orders_response.data) if orders_response.data else 0
        total_revenue = sum(float(order['total_amount']) for order in orders_response.data) if orders_response.data else 0
        
        today = datetime.now().date()
        today_orders = [order for order in orders_response.data if datetime.fromisoformat(order['created_at'].replace('Z', '+00:00')).date() == today] if orders_response.data else []
        today_count = len(today_orders)
        today_revenue = sum(float(order['total_amount']) for order in today_orders)
        
        return jsonify({
            'success': True,
            'stats': {
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'today_orders': today_count,
                'today_revenue': today_revenue
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
