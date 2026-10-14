"""Reglas del negocio: independientes de la pantalla y fáciles de probar."""
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import csv


def parse_money(value):
    """Acepta '12.50' o '12,50'; devuelve centavos enteros."""
    try:
        number = Decimal(str(value).strip().replace(',', '.'))
        if not number.is_finite() or number <= 0:
            raise ValueError('El monto debe ser mayor que cero.')
        if number.as_tuple().exponent < -2:
            raise ValueError('Escribe como máximo dos decimales.')
        cents = int((number * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        if cents > 100_000_000_00:
            raise ValueError('El monto es demasiado grande.')
        return cents
    except (InvalidOperation, TypeError):
        raise ValueError('Introduce un monto válido, por ejemplo 4.50.')


def money(cents):
    return f'${cents / 100:,.2f}'


def check_date(value):
    try:
        result = date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError('Usa el formato de fecha AAAA-MM-DD.')
    if result > date.today():
        raise ValueError('La fecha no puede estar en el futuro.')
    return result.isoformat()


class Finance:
    def __init__(self, db):
        self.db = db

    def categories(self, kind):
        return self.db.query('SELECT * FROM categories WHERE kind=? ORDER BY name', (kind,))

    def totals(self):
        rows = self.db.query('SELECT kind, COALESCE(SUM(cents),0) amount FROM movements GROUP BY kind')
        mapping = {r['kind']: r['amount'] for r in rows}
        income, expense = mapping.get('ingreso', 0), mapping.get('gasto', 0)
        reserved = self.db.one('SELECT COALESCE(SUM(cents),0) amount FROM contributions')['amount']
        return dict(income=income, expense=expense, balance=income-expense,
                    reserved=reserved, available=income-expense-reserved)

    def movement(self, kind, amount, category_id, description, when, movement_id=None):
        if kind not in ('ingreso', 'gasto'):
            raise ValueError('Tipo de movimiento incorrecto.')
        cents = parse_money(amount)
        when = check_date(when)
        description = description.strip()
        if not (2 <= len(description) <= 90):
            raise ValueError('La descripción debe tener entre 2 y 90 caracteres.')
        cat = self.db.one('SELECT id FROM categories WHERE id=? AND kind=?', (category_id,kind))
        if not cat:
            raise ValueError('Selecciona una categoría válida.')
        old = None
        if movement_id is not None:
            old = self.db.one('SELECT * FROM movements WHERE id=?', (movement_id,))
            if old is None:
                raise ValueError('El movimiento ya no existe.')
        available = self.totals()['available']
        if old:
            available += old['cents'] if old['kind'] == 'gasto' else -old['cents']
        prospective = available + (cents if kind == 'ingreso' else -cents)
        if prospective < 0:
            raise ValueError('No hay dinero disponible suficiente. Revisa el ahorro reservado.')
        if old:
            self.db.execute('''UPDATE movements SET kind=?, cents=?, category_id=?,description=?,movement_date=?
                WHERE id=?''', (kind,cents,category_id,description,when,movement_id))
        else:
            self.db.execute('''INSERT INTO movements(kind,cents,category_id,description,movement_date)
                VALUES (?,?,?,?,?)''', (kind,cents,category_id,description,when))

    def delete_movement(self, movement_id):
        old = self.db.one('SELECT * FROM movements WHERE id=?', (movement_id,))
        if old is None:
            return
        if old['kind'] == 'ingreso' and self.totals()['available'] < old['cents']:
            raise ValueError('No puedes borrar este ingreso: dejaría el saldo disponible negativo.')
        self.db.execute('DELETE FROM movements WHERE id=?', (movement_id,))

    def movements(self, kind=None, month=None):
        conditions, args = [], []
        if kind in ('ingreso', 'gasto'):
            conditions.append('m.kind=?'); args.append(kind)
        if month:
            conditions.append('substr(m.movement_date,1,7)=?'); args.append(month)
        where = 'WHERE ' + ' AND '.join(conditions) if conditions else ''
        return self.db.query('''SELECT m.*,c.name category FROM movements m
            JOIN categories c ON c.id=m.category_id '''+where+'''
            ORDER BY m.movement_date DESC,m.id DESC''', args)

    def add_goal(self, name, amount):
        name = name.strip()
        if not 3 <= len(name) <= 70:
            raise ValueError('La meta debe tener entre 3 y 70 caracteres.')
        self.db.execute('INSERT INTO goals(name,target_cents) VALUES (?,?)',(name,parse_money(amount)))

    def goals(self):
        return self.db.query('''SELECT g.id,g.name,g.target_cents,
           COALESCE(SUM(c.cents),0) saved FROM goals g
           LEFT JOIN contributions c ON c.goal_id=g.id
           GROUP BY g.id ORDER BY g.id DESC''')

    def contribute(self, goal_id, amount):
        cents = parse_money(amount)
        goal = next((g for g in self.goals() if g['id']==goal_id), None)
        if goal is None: raise ValueError('La meta no existe.')
        if cents > goal['target_cents']-goal['saved']:
            raise ValueError('El aporte supera el dinero que falta para esta meta.')
        if cents > self.totals()['available']:
            raise ValueError('No tienes saldo disponible suficiente para reservar este ahorro.')
        self.db.execute('INSERT INTO contributions(goal_id,cents,contribution_date) VALUES (?,?,?)',
                        (goal_id,cents,date.today().isoformat()))

    def delete_goal(self, goal_id):
        # Al borrar la meta, sus aportes se liberan como saldo disponible.
        self.db.execute('DELETE FROM goals WHERE id=?',(goal_id,))

    def monthly(self, month):
        rows = self.db.query('''SELECT kind, COALESCE(SUM(cents),0) amount FROM movements
             WHERE substr(movement_date,1,7)=? GROUP BY kind''',(month,))
        d = {r['kind']:r['amount'] for r in rows}
        return d.get('ingreso',0),d.get('gasto',0)

    def spending_by_category(self, month):
        return self.db.query('''SELECT c.name, SUM(m.cents) amount FROM movements m
            JOIN categories c ON c.id=m.category_id
            WHERE m.kind='gasto' AND substr(m.movement_date,1,7)=?
            GROUP BY c.id ORDER BY amount DESC''',(month,))

    def streak(self):
        dates = {date.fromisoformat(r['movement_date']) for r in self.db.query(
            'SELECT DISTINCT movement_date FROM movements')}
        today = date.today()
        cursor = today if today in dates else today-timedelta(days=1)
        count = 0
        while cursor in dates:
            count += 1; cursor -= timedelta(days=1)
        return count

    def badges(self):
        t = self.totals(); count = len(self.movements()); goals = self.goals()
        return [
          ('Primer paso',count>=1,'Registra tu primer movimiento'),
          ('Explorador',count>=10,'Registra 10 movimientos'),
          ('Ahorrador',t['reserved']>=1000,'Reserva al menos $10'),
          ('Meta cumplida',any(g['saved']>=g['target_cents'] for g in goals),'Completa una meta'),
          ('Constancia',self.streak()>=3,'Registra movimientos durante 3 días seguidos'),
        ]

    def export_csv(self, path):
        with open(path,'w',newline='',encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['Fecha','Tipo','Categoría','Descripción','Monto USD'])
            for r in self.movements():
                writer.writerow([r['movement_date'],r['kind'],r['category'],r['description'],
                                 f"{r['cents']/100:.2f}"])
