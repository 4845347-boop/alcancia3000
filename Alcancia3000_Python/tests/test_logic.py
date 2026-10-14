import tempfile
import unittest
from pathlib import Path
from datetime import date
from database import Database
from logic import Finance, parse_money

class FinanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=Database(Path(self.tmp.name)/'test.db')
        self.f=Finance(self.db)
        self.income=self.f.categories('ingreso')[0]['id']
        self.expense=self.f.categories('gasto')[0]['id']
        self.day=date.today().isoformat()

    def tearDown(self):
        self.db.close();self.tmp.cleanup()

    def test_money_validations(self):
        self.assertEqual(parse_money('2,50'),250)
        for v in ['-2','0','abc','1.123']:
            with self.assertRaises(ValueError): parse_money(v)

    def test_balance_goal_and_no_double_count(self):
        self.f.movement('ingreso','20',self.income,'Mesada',self.day)
        self.f.movement('gasto','3',self.expense,'Autobús',self.day)
        self.f.add_goal('Audífonos','10')
        goal=self.f.goals()[0]
        self.f.contribute(goal['id'],'5')
        self.assertEqual(self.f.totals(),{'income':2000,'expense':300,'balance':1700,'reserved':500,'available':1200})
        with self.assertRaises(ValueError):self.f.movement('gasto','13',self.expense,'Demasiado',self.day)
        self.assertEqual(self.f.goals()[0]['saved'],500)

    def test_persistence_edit_and_delete(self):
        self.f.movement('ingreso','15',self.income,'Regalo',self.day)
        mid=self.f.movements()[0]['id']
        self.f.movement('ingreso','18',self.income,'Regalo corregido',self.day,mid)
        self.assertEqual(self.f.totals()['income'],1800)
        self.db.close();self.db=Database(Path(self.tmp.name)/'test.db');self.f=Finance(self.db)
        self.assertEqual(self.f.totals()['income'],1800)
        self.f.delete_movement(mid)
        self.assertEqual(self.f.totals()['income'],0)

    def test_badge_and_streak(self):
        self.f.movement('ingreso','1',self.income,'Mesada',self.day)
        self.assertEqual(self.f.streak(),1)
        self.assertTrue(self.f.badges()[0][1])

    def test_cannot_delete_income_backing_reserved_savings(self):
        self.f.movement('ingreso','10',self.income,'Mesada',self.day)
        mid=self.f.movements()[0]['id'];self.f.add_goal('Libros','10')
        self.f.contribute(self.f.goals()[0]['id'],'9')
        with self.assertRaises(ValueError):self.f.delete_movement(mid)

if __name__=='__main__':unittest.main()
