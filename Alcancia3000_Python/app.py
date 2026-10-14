"""Alcancía 3000 - interfaz de escritorio (Tkinter, sin paquetes externos)."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
from database import Database
from logic import Finance, money

BG='#0B1425'; PANEL='#132239'; PANEL2='#1C304B'; TEXT='#F0F6FF'; MUTED='#9BAEC8'
MINT='#35D6A6'; GOLD='#F3C969'; RED='#FF8C9A'; BLUE='#72B5F7'
FONT='Segoe UI'

class Alcancia(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Alcancía 3000 | Tu dinero, tu futuro')
        self.geometry('1120x730'); self.minsize(860,600); self.configure(bg=BG)
        self.db=Database(); self.finance=Finance(self.db)
        self.page='Inicio'; self.selected_id=None
        self.style=ttk.Style(self); self.style.theme_use('clam')
        self.style.configure('Dark.Treeview',background=PANEL,fieldbackground=PANEL,foreground=TEXT,
                             rowheight=31,borderwidth=0,font=(FONT,10))
        self.style.configure('Dark.Treeview.Heading',background=PANEL2,foreground=TEXT,font=(FONT,10,'bold'))
        self.style.map('Dark.Treeview',background=[('selected','#285F6B')],foreground=[('selected','white')])
        self.sidebar=tk.Frame(self,bg='#101C30',width=205);self.sidebar.pack(side='left',fill='y');self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar,text='◈  ALCANCÍA',bg='#101C30',fg=MINT,font=(FONT,17,'bold')).pack(padx=18,pady=(32,4),anchor='w')
        tk.Label(self.sidebar,text='3000  •  EDICIÓN ESTUDIANTIL',bg='#101C30',fg=MUTED,font=(FONT,9)).pack(padx=19,pady=(0,34),anchor='w')
        self.nav={}
        for name,symbol in [('Inicio','⌂'),('Movimientos','⇄'),('Metas','◎'),('Estadísticas','▥'),('Logros','★')]:
            b=tk.Button(self.sidebar,text=f' {symbol}   {name}',font=(FONT,11,'bold'),anchor='w',padx=17,
                        bg='#101C30',fg=TEXT,activebackground=PANEL2,activeforeground=MINT,
                        bd=0,relief='flat',cursor='hand2',command=lambda n=name:self.show(n))
            b.pack(fill='x',padx=9,pady=4,ipady=11); self.nav[name]=b
        tk.Label(self.sidebar,text='● FUNCIONA SIN INTERNET\nDatos guardados en este equipo',bg='#101C30',
                 fg=MUTED,font=(FONT,9),justify='left').pack(side='bottom',anchor='w',padx=15,pady=24)
        self.main=tk.Frame(self,bg=BG);self.main.pack(side='left',fill='both',expand=True)
        self.protocol('WM_DELETE_WINDOW',self.close)
        self.show('Inicio')

    def close(self):
        self.db.close();self.destroy()

    def label(self,parent,text,size=11,color=TEXT,bold=False,**kwargs):
        return tk.Label(parent,text=text,bg=parent.cget('bg'),fg=color,
                        font=(FONT,size,'bold' if bold else 'normal'),**kwargs)

    def button(self,parent,text,command,accent=False):
        return tk.Button(parent,text=text,command=command,bg=MINT if accent else PANEL2,
              fg=BG if accent else TEXT,activebackground=BLUE,activeforeground=BG,
              relief='flat',bd=0,padx=17,pady=9,cursor='hand2',font=(FONT,10,'bold'))

    def entry(self,parent,width=23):
        return tk.Entry(parent,width=width,bg='#243650',fg=TEXT,insertbackground=TEXT,
                        relief='flat',font=(FONT,11),highlightthickness=1,highlightbackground='#38516D')

    def section(self,parent,pady=14):
        frame=tk.Frame(parent,bg=PANEL,padx=19,pady=pady,highlightbackground='#2A3D55',highlightthickness=1)
        return frame

    def show(self,name):
        self.page=name
        for key,btn in self.nav.items(): btn.configure(bg=PANEL2 if key==name else '#101C30',fg=MINT if key==name else TEXT)
        for child in self.main.winfo_children(): child.destroy()
        head=tk.Frame(self.main,bg=BG);head.pack(fill='x',padx=32,pady=(25,17))
        self.label(head,name,23,bold=True).pack(side='left')
        self.label(head,date.today().strftime('%d/%m/%Y')+'  •  USD',10,MUTED).pack(side='right')
        content=tk.Frame(self.main,bg=BG);content.pack(fill='both',expand=True,padx=32,pady=(0,24))
        {'Inicio':self.dashboard,'Movimientos':self.movements_page,'Metas':self.goals_page,
         'Estadísticas':self.stats_page,'Logros':self.badges_page}[name](content)

    def dashboard(self,root):
        self.label(root,'Cada dólar cuenta. Conoce tus hábitos y haz crecer tus ahorros.',11,MUTED).pack(anchor='w',pady=(0,16))
        t=self.finance.totals();cards=tk.Frame(root,bg=BG);cards.pack(fill='x')
        info=[('INGRESOS',t['income'],MINT),('GASTOS',t['expense'],RED),('RESERVADO',t['reserved'],GOLD),('DISPONIBLE',t['available'],BLUE)]
        for title,value,color in info:
            box=self.section(cards,18);box.pack(side='left',fill='both',expand=True,padx=(0,9))
            self.label(box,title,9,MUTED,True).pack(anchor='w')
            self.label(box,money(value),19,color,True).pack(anchor='w',pady=(6,1))
        actions=self.section(root);actions.pack(fill='x',pady=20)
        self.label(actions,'Acciones rápidas',14,bold=True).pack(anchor='w',pady=(0,11))
        br=tk.Frame(actions,bg=PANEL);br.pack(anchor='w')
        self.button(br,'+ Registrar ingreso',lambda:self.movement_dialog('ingreso'),True).pack(side='left',padx=(0,10))
        self.button(br,'− Registrar gasto',lambda:self.movement_dialog('gasto')).pack(side='left',padx=(0,10))
        self.button(br,'◎ Crear meta',self.goal_dialog).pack(side='left')
        goals=self.finance.goals(); block=self.section(root);block.pack(fill='x')
        self.label(block,'Tu progreso de ahorro',14,bold=True).pack(anchor='w',pady=(0,13))
        if not goals:self.label(block,'Todavía no tienes metas. ¡Crea una para empezar!',11,MUTED).pack(anchor='w')
        for g in goals[:3]:
            row=tk.Frame(block,bg=PANEL);row.pack(fill='x',pady=5)
            ratio=min(1,g['saved']/g['target_cents'])
            self.label(row,f"{g['name']}   {money(g['saved'])} / {money(g['target_cents'])}",10).pack(anchor='w')
            bar=tk.Canvas(row,height=12,bg=PANEL,highlightthickness=0)
            bar.pack(fill='x',pady=4)
            def draw(ev,b=bar,r=ratio):
                b.delete('all');b.create_rectangle(0,0,ev.width,12,fill=PANEL2,outline='')
                b.create_rectangle(0,0,max(0,ev.width*r),12,fill=MINT,outline='')
            bar.bind('<Configure>',draw)
        self.label(root,f"🔥 Racha actual: {self.finance.streak()} día(s)   •   ⭐ Logros: {sum(x[1] for x in self.finance.badges())}/5",
                   11,GOLD).pack(anchor='w',pady=15)

    def table(self,root,columns,widths):
        wrap=tk.Frame(root,bg=PANEL);wrap.pack(fill='both',expand=True,pady=12)
        tree=ttk.Treeview(wrap,columns=columns,show='headings',style='Dark.Treeview',selectmode='browse')
        for col,w in zip(columns,widths):tree.heading(col,text=col);tree.column(col,width=w,stretch=True)
        scroll=ttk.Scrollbar(wrap,orient='vertical',command=tree.yview);tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y');tree.pack(side='left',fill='both',expand=True)
        return tree

    def movements_page(self,root):
        top=tk.Frame(root,bg=BG);top.pack(fill='x')
        self.button(top,'+ Ingreso',lambda:self.movement_dialog('ingreso'),True).pack(side='left',padx=(0,9))
        self.button(top,'− Gasto',lambda:self.movement_dialog('gasto')).pack(side='left')
        self.button(top,'Exportar CSV',self.export).pack(side='right')
        cols=('ID','Fecha','Tipo','Categoría','Descripción','Monto')
        tree=self.table(root,cols,[45,90,85,125,210,90])
        for r in self.finance.movements():
            tree.insert('', 'end',values=(r['id'],r['movement_date'],r['kind'].capitalize(),r['category'],r['description'],money(r['cents'])))
        br=tk.Frame(root,bg=BG);br.pack(anchor='w')
        def current():
            selected=tree.selection()
            if not selected:messagebox.showinfo('Selecciona','Selecciona un movimiento de la tabla.');return None
            return int(tree.item(selected[0],'values')[0])
        def edit():
            mid=current()
            if mid is not None:self.movement_dialog(movement_id=mid)
        def remove():
            mid=current()
            if mid is None:return
            if messagebox.askyesno('Confirmar','¿Eliminar este movimiento?'):
                try:self.finance.delete_movement(mid);self.show('Movimientos')
                except ValueError as err:messagebox.showerror('Validación',str(err))
        self.button(br,'Editar selección',edit).pack(side='left',padx=(0,9))
        self.button(br,'Eliminar selección',remove).pack(side='left')

    def dialog(self,title):
        win=tk.Toplevel(self);win.title(title);win.configure(bg=PANEL);win.geometry('415x455')
        win.transient(self);win.grab_set();win.resizable(False,False)
        body=tk.Frame(win,bg=PANEL,padx=28,pady=20);body.pack(fill='both',expand=True)
        self.label(body,title,17,bold=True).pack(anchor='w',pady=(0,15))
        return win,body

    def field(self,body,title,default=''):
        self.label(body,title,10,MUTED).pack(anchor='w',pady=(10,4))
        e=self.entry(body,37);e.pack(fill='x',ipady=7);e.insert(0,str(default));return e

    def movement_dialog(self,kind='gasto',movement_id=None):
        old=self.db.one('SELECT * FROM movements WHERE id=?',(movement_id,)) if movement_id else None
        if old:kind=old['kind']
        win,body=self.dialog('Editar movimiento' if old else 'Nuevo '+kind)
        amount=self.field(body,'Monto en USD',f"{old['cents']/100:.2f}" if old else '')
        desc=self.field(body,'Descripción',old['description'] if old else '')
        when=self.field(body,'Fecha (AAAA-MM-DD)',old['movement_date'] if old else date.today().isoformat())
        self.label(body,'Categoría',10,MUTED).pack(anchor='w',pady=(10,4))
        categories=self.finance.categories(kind)
        by_name={r['name']:r['id'] for r in categories}
        selected=next((r['name'] for r in categories if old and r['id']==old['category_id']),categories[0]['name'])
        combo=ttk.Combobox(body,values=list(by_name),state='readonly',font=(FONT,11));combo.set(selected);combo.pack(fill='x')
        def save():
            try:self.finance.movement(kind,amount.get(),by_name[combo.get()],desc.get(),when.get(),movement_id)
            except (ValueError,KeyError) as err:messagebox.showerror('Revisa los datos',str(err),parent=win);return
            win.destroy();self.show(self.page)
        self.button(body,'Guardar movimiento',save,True).pack(fill='x',pady=(22,0))

    def goals_page(self,root):
        row=tk.Frame(root,bg=BG);row.pack(fill='x')
        self.button(row,'+ Nueva meta',self.goal_dialog,True).pack(side='left')
        self.label(root,'Un aporte reserva parte de tu saldo: no cuenta como gasto y evita usar ese dinero.',10,MUTED).pack(anchor='w',pady=12)
        goals=self.finance.goals()
        if not goals:self.label(root,'Aún no tienes metas. ¡Comienza con algo que te motive!',12,MUTED).pack(anchor='w')
        for g in goals:
            box=self.section(root,12);box.pack(fill='x',pady=6)
            line=tk.Frame(box,bg=PANEL);line.pack(fill='x')
            self.label(line,g['name'],13,bold=True).pack(side='left')
            ratio=g['saved']/g['target_cents']
            self.label(line,f"{money(g['saved'])} / {money(g['target_cents'])}  •  {ratio:.0%}",11,MINT).pack(side='right')
            progress=ttk.Progressbar(box,maximum=100,value=ratio*100);progress.pack(fill='x',pady=8)
            buttons=tk.Frame(box,bg=PANEL);buttons.pack(anchor='w')
            self.button(buttons,'+ Aportar',lambda gid=g['id']:self.contribute_dialog(gid)).pack(side='left',padx=(0,9))
            self.button(buttons,'Eliminar meta',lambda gid=g['id']:self.remove_goal(gid)).pack(side='left')

    def goal_dialog(self):
        win,body=self.dialog('Nueva meta de ahorro');win.geometry('415x320')
        name=self.field(body,'¿Qué quieres conseguir? (ej.: bicicleta)')
        amount=self.field(body,'¿Cuánto necesitas en USD?')
        def save():
            try:self.finance.add_goal(name.get(),amount.get())
            except ValueError as err:messagebox.showerror('Validación',str(err),parent=win);return
            win.destroy();self.show(self.page)
        self.button(body,'Crear meta',save,True).pack(fill='x',pady=22)

    def contribute_dialog(self,goal_id):
        win,body=self.dialog('Apartar dinero para ahorrar');win.geometry('415x265')
        amount=self.field(body,'Monto a reservar en USD')
        def save():
            try:self.finance.contribute(goal_id,amount.get())
            except ValueError as err:messagebox.showerror('Validación',str(err),parent=win);return
            win.destroy();self.show(self.page)
        self.button(body,'Confirmar aporte',save,True).pack(fill='x',pady=22)

    def remove_goal(self,goal_id):
        if messagebox.askyesno('Eliminar meta','¿Eliminar meta y liberar sus ahorros reservados?'):
            self.finance.delete_goal(goal_id);self.show('Metas')

    def stats_page(self,root):
        current=date.today().strftime('%Y-%m');row=tk.Frame(root,bg=BG);row.pack(fill='x')
        self.label(row,'Mes (AAAA-MM): ',11).pack(side='left')
        month=self.entry(row,9);month.insert(0,current);month.pack(side='left',ipady=6)
        chart=self.section(root);chart.pack(fill='both',expand=True,pady=16)
        def redraw():
            m=month.get().strip()
            try:date.fromisoformat(m+'-01')
            except ValueError:messagebox.showerror('Mes inválido','Utiliza AAAA-MM.');return
            for c in chart.winfo_children():c.destroy()
            income,expense=self.finance.monthly(m)
            self.label(chart,f'Ingresos: {money(income)}     Gastos: {money(expense)}',14,bold=True).pack(anchor='w')
            self.label(chart,'Distribución de gastos por categoría',12,MUTED).pack(anchor='w',pady=(22,12))
            data=self.finance.spending_by_category(m)
            if not data:self.label(chart,'Sin gastos registrados en este mes.',11,MUTED).pack(anchor='w');return
            maxval=max(r['amount'] for r in data)
            for r in data:
                holder=tk.Frame(chart,bg=PANEL);holder.pack(fill='x',pady=7)
                self.label(holder,f"{r['name']}   {money(r['amount'])}",10).pack(anchor='w')
                bar=tk.Canvas(holder,height=18,bg=PANEL,highlightthickness=0);bar.pack(fill='x',pady=3)
                frac=r['amount']/maxval
                def draw(e,b=bar,f=frac):
                    b.delete('all');b.create_rectangle(0,0,e.width,18,fill=PANEL2,outline='')
                    b.create_rectangle(0,0,e.width*f,18,fill=MINT,outline='')
                bar.bind('<Configure>',draw)
        self.button(row,'Consultar',redraw,True).pack(side='left',padx=10)
        redraw()

    def badges_page(self,root):
        self.label(root,f"🔥 Racha de registro: {self.finance.streak()} días",14,GOLD,True).pack(anchor='w',pady=(0,13))
        self.label(root,'RETO DE LA SEMANA  •  Registra tus movimientos durante 3 días seguidos.',11,MUTED).pack(anchor='w',pady=(0,20))
        for name,unlocked,description in self.finance.badges():
            box=self.section(root,13);box.pack(fill='x',pady=5)
            line=tk.Frame(box,bg=PANEL);line.pack(fill='x')
            self.label(line,('★  ' if unlocked else '◇  ')+name,13,MINT if unlocked else MUTED,True).pack(side='left')
            self.label(line,'DESBLOQUEADO' if unlocked else 'PENDIENTE',9,MINT if unlocked else MUTED,True).pack(side='right')
            self.label(box,description,10,MUTED).pack(anchor='w')

    def export(self):
        path=filedialog.asksaveasfilename(title='Exportar tus movimientos',defaultextension='.csv',
                filetypes=[('Archivo CSV','*.csv')],initialfile='movimientos_alcancia3000.csv')
        if path:
            try:self.finance.export_csv(path);messagebox.showinfo('Listo','Movimientos exportados correctamente.')
            except OSError as err:messagebox.showerror('Error al exportar',str(err))

if __name__=='__main__':
    Alcancia().mainloop()
