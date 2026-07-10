from decimal import Decimal
from datetime import datetime
from models.database import connect_to_database


class Order:
    def __init__(self, order_id=None, reservation_id=None, customer_id=None, table_id=None,
                 employee_id=None, order_date=None, total_amount=0.00, discount_percent=0.00,
                 discount_amount=0.00, final_amount=0.00, status='Pending'):
        self.order_id = order_id
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.table_id = table_id
        self.employee_id = employee_id
        self.order_date = order_date
        self.total_amount = Decimal(str(total_amount)) if total_amount is not None else Decimal('0.00')
        self.discount_percent = Decimal(str(discount_percent)) if discount_percent is not None else Decimal('0.00')
        self.discount_amount = Decimal(str(discount_amount)) if discount_amount is not None else Decimal('0.00')
        self.final_amount = Decimal(str(final_amount)) if final_amount is not None else Decimal('0.00')
        self.status = status

    @staticmethod
    def _get_connection():
        conn = connect_to_database()
        if conn is None:
            raise ConnectionError('Không thể kết nối tới cơ sở dữ liệu SQL Server')
        return conn

    @classmethod
    def create_order(cls, customer_id, table_id, employee_id=None, reservation_id=None,
                     items=None, discount_percent=0.00, status='Pending'):
        if not customer_id:
            raise ValueError('Thiếu CustomerID')
        if not table_id:
            raise ValueError('Thiếu TableID')
        if items is None:
            items = []

        conn = cls._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Orders (ReservationID, CustomerID, TableID, EmployeeID, DiscountPercent, Status)
                OUTPUT INSERTED.OrderID
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                reservation_id,
                customer_id,
                table_id,
                employee_id,
                Decimal(str(discount_percent)),
                status,
            )
            row = cursor.fetchone()
            if not row:
                raise RuntimeError('Không thể tạo đơn hàng')
            order_id = row[0]

            total_amount = Decimal('0.00')
            for item in items:
                item_id = item.get('item_id')
                quantity = item.get('quantity', 1)
                if not item_id:
                    continue

                cursor.execute(
                    "SELECT Price FROM MenuItems WHERE ItemID = ?",
                    item_id,
                )
                price_row = cursor.fetchone()
                unit_price = Decimal(str(price_row[0])) if price_row and price_row[0] is not None else Decimal('0.00')
                sub_total = unit_price * Decimal(quantity)
                total_amount += sub_total

                cursor.execute(
                    """
                    INSERT INTO OrderDetails (OrderID, ItemID, Quantity, UnitPrice, SubTotal)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    order_id,
                    item_id,
                    quantity,
                    unit_price,
                    sub_total,
                )

            discount_amount = total_amount * Decimal(str(discount_percent)) / Decimal('100')
            final_amount = total_amount - discount_amount
            cursor.execute(
                """
                UPDATE Orders
                SET TotalAmount = ?, DiscountAmount = ?, FinalAmount = ?, Status = ?
                WHERE OrderID = ?
                """,
                total_amount,
                discount_amount,
                final_amount,
                status,
                order_id,
            )
            conn.commit()
            return cls(order_id=order_id, reservation_id=reservation_id, customer_id=customer_id,
                      table_id=table_id, employee_id=employee_id, total_amount=total_amount,
                      discount_percent=discount_percent, discount_amount=discount_amount,
                      final_amount=final_amount, status=status)
        finally:
            conn.close()

    @classmethod
    def get_order_by_id(cls, order_id):
        conn = cls._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT OrderID, ReservationID, CustomerID, TableID, EmployeeID,
                       OrderDate, TotalAmount, DiscountPercent, DiscountAmount,
                       FinalAmount, Status
                FROM Orders
                WHERE OrderID = ?
                """,
                order_id,
            )
            row = cursor.fetchone()
            if not row:
                return None
            return cls(
                order_id=row[0],
                reservation_id=row[1],
                customer_id=row[2],
                table_id=row[3],
                employee_id=row[4],
                order_date=row[5],
                total_amount=row[6],
                discount_percent=row[7],
                discount_amount=row[8],
                final_amount=row[9],
                status=row[10],
            )
        finally:
            conn.close()

    @classmethod
    def get_order_items(cls, order_id):
        conn = cls._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT od.OrderDetailID, od.ItemID, mi.ItemName, od.Quantity, od.UnitPrice, od.SubTotal
                FROM OrderDetails od
                JOIN MenuItems mi ON od.ItemID = mi.ItemID
                WHERE od.OrderID = ?
                ORDER BY od.OrderDetailID
                """,
                order_id,
            )
            return cursor.fetchall()
        finally:
            conn.close()

    @classmethod
    def get_all_orders(cls):
        conn = cls._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT OrderID, ReservationID, CustomerID, TableID, EmployeeID,
                       OrderDate, TotalAmount, DiscountPercent, DiscountAmount,
                       FinalAmount, Status
                FROM Orders
                ORDER BY OrderID DESC
                """
            )
            rows = cursor.fetchall()
            return [
                cls(
                    order_id=row[0],
                    reservation_id=row[1],
                    customer_id=row[2],
                    table_id=row[3],
                    employee_id=row[4],
                    order_date=row[5],
                    total_amount=row[6],
                    discount_percent=row[7],
                    discount_amount=row[8],
                    final_amount=row[9],
                    status=row[10],
                )
                for row in rows
            ]
        finally:
            conn.close()

    @classmethod
    def update_status(cls, order_id, status):
        if not order_id:
            raise ValueError('Thiếu OrderID')
        allowed = ['Pending', 'Đang làm', 'Đã xong']
        if status not in allowed:
            raise ValueError('Trạng thái không hợp lệ')
        conn = cls._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Orders SET Status = ? WHERE OrderID = ?", status, order_id)
            conn.commit()
            return True
        finally:
            conn.close()

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'reservation_id': self.reservation_id,
            'customer_id': self.customer_id,
            'table_id': self.table_id,
            'employee_id': self.employee_id,
            'order_date': self.order_date,
            'total_amount': float(self.total_amount),
            'discount_percent': float(self.discount_percent),
            'discount_amount': float(self.discount_amount),
            'final_amount': float(self.final_amount),
            'status': self.status,
        }
