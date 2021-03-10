# -*- coding: utf-8 -*-

import tkinter as tk
import math
# TODO: read documentation
from sympy import *

x, y, z = symbols('x y z')
SYMBOLS = {'x', 'y', 'z'}

init_printing()

# https://stackoverflow.com/questions/37754756/can-i-integrate-mathjax-into-a-python-program
# https://docs.sympy.org/latest/tutorial/index.html


FUNCS = {
	'Integral' : (
		'Integral(функция)',
		'Вычисляет интеграл из переданной функции'
	),
	'Limit' : (
		'Limit(функция, значение, стремится к...)',
		'Предел функции стремящейся к заданному значению'
	),
	'sqrt' : (
		'sqrt(подкоренное выражение)',
		'Вычисляет корень квадратный из подкоренного выражения'
	),
	'exp' : (
		'exp(степень)',
		'Экспонента'
	),
	'sin' : (
		'sin(число)',
		'Синус числа'
	),
	'cos' : (
		'cos(число)',
		'Косинус числа'
	),
	'tg' : (
		'tg(число)',
		'Тангенс числа'
	),
	'Derivative' : (
		'Derivative(функцияю, *производная от числа)',
		'''Вычисляет производную от функции для переданных чисел.
Например: diff(x**4, x, 3). Вычисляет третью производную от x^4'''
	)
}


class Window(tk.Tk):
	def __init__(self):
		super().__init__()

		self.title('Задание для реферата')
		self.geometry('400x250+50+350')

		self.init_ui()


	def init_ui(self):
		# ========
		# = MENU =
		menu = tk.Menu(self)
		self.config(menu=menu)

		# Create settings folder and add to main menu
		settings_item = tk.Menu(menu, tearoff=0)
		menu.add_cascade(label='Настройки', menu=settings_item)

		# Add commands to settings folder
		settings_item.add_command(
			label = 'Неизвестные',
			command = self.__open_symbol_list
		)
		# ========

		# ===========
		# = TOOLBAR =
		toolbar = tk.Frame(self, bg='#fff')
		toolbar.place(x=0, y=0, relwidth=1, relheight=.1)

		# = FORMULA =
		tk.Button(toolbar, text='f(x)=', font='Arial 12 italic',
			bg='#fff', command=self.__open_func_list).place(
			relx=.05, rely=.1, relwidth=.1, relheight=.8)
		self.func = tk.Entry(toolbar, font='Arial 12')
		self.func.place(relx=.15, rely=.1, relwidth=.75, relheight=.8)
		self.func.bind('<Key>', lambda e: self.__update_formula(
			self.func.get())
		)
		# ===========

		# ================
		# = SHOW FORMULA =
		show = tk.Frame(self, bg='lightgrey')
		show.place(x=0, rely=.1, relwidth=1, relheight=.8)

		scr_x_formula = tk.Scrollbar(show, orient=tk.HORIZONTAL)
		scr_x_formula.pack(side='bottom', fill='x')
		wrapper = tk.Canvas(show, bg='lightgrey', 
			xscrollcommand=scr_x_formula.set)
		wrapper.pack(side='top', fill='both', expand=tk.ON)

		self.formula = tk.Label(wrapper, text='',
			anchor='center', font=('Lucida Console', 10))
		self.formula.pack(side='left', fill='both', expand=tk.ON)

		scr_x_formula['command'] = wrapper.xview
		# ================

		# ==========
		# = OUTPUT =
		output = tk.Frame(self, bg='#fff')
		output.place(x=0, rely=.9, relwidth=1, relheight=.1)
		calc = tk.Button(output, text='Calc', relief=tk.FLAT)
		calc.pack(side='left', padx=5, pady=5)
		# TODO: Create func for show calculate
		# ==========


	def __open_func_list(self):
		def update_info():
			ind = func_list.curselection()

			if len(ind):
				# use['text'] = FUNCS.get(func_list.get(ind))[0]
				use['state'] = tk.NORMAL
				use.delete(1.0, tk.END)
				use.insert(1.0, FUNCS.get(func_list.get(ind))[0])
				use['state'] = tk.DISABLED

				#info['text'] = FUNCS.get(func_list.get(ind))[1]
				info['state'] = tk.NORMAL
				info.delete(1.0, tk.END)
				info.insert(1.0, FUNCS.get(func_list.get(ind))[1])
				info['state'] = tk.DISABLED


		def add_func():
			ind = func_list.curselection()

			if len(ind):
				start = self.func.index(tk.INSERT)
				form = func_list.get(ind) + '()'
				self.func.insert(start, form)
				self.func.icursor(start + len(form) - 1)


		# ==========
		# = WINDOW =
		funcs = tk.Toplevel()
		funcs.title('Funcs')

		# = LEFT LIST =
		func_list = tk.Listbox(funcs)
		func_list.place(relx=.05, rely=.05, relwidth=.4, relheight=.9)
		func_list.bind('<<ListboxSelect>>', lambda e: update_info())

		for item in FUNCS.keys():
			func_list.insert(tk.END, item)

		# = RIGHT INFO =
		fr_info = tk.LabelFrame(funcs, text='Information')
		fr_info.place(relx=.55, rely=.05, relwidth=.4, relheight=.75)
		use = tk.Text(fr_info, state=tk.DISABLED, bg='#f0f0f0')
		use.place(x=0, y=0, relwidth=1, relheight=.5)
		info = tk.Text(fr_info, state=tk.DISABLED, bg='#f0f0f0')
		info.place(x=0, rely=.5, relwidth=1, relheight=.5)

		add = tk.Button(funcs, text='>>>', command=add_func)
		add.place(relx=.6, rely=.85, relwidth=.3, relheight=.1)

		funcs.mainloop()
		# ==========


	def __update_formula(self, formula):
		# TODO: Update formulas in best format
		try:
			if formula == 'Демон на 4 с минусом':
				self.formula['fg'] = '#000'
				self.formula['text'] = '(｡’▽’｡)♥'
			else:
				self.formula['fg'] = '#000'
				self.formula['text'] = pretty(
					eval(formula),
					use_unicode=False
				)
		except:
			self.formula['fg'] = 'red'
			self.formula['text'] = '[Ошибка в формуле]'


	def __open_symbol_list(self):
		def add_sym():
			SYMBOLS.add(sym.get())
			sym_list.delete(0, tk.END)

			for item in sorted(SYMBOLS):
				sym_list.insert(tk.END, item)

			# x, y, z = symbols('x y z')
			e_str = '%s()'
			#for symbol in SYMBOLS:
			#	e_str

			for i in SYMBOLS:
				print(i)

			# TODO: Update values to formulas


		top_win = tk.Toplevel()
		top_win.title('Symbols list')

		tk.Label(top_win, text='Enter symbol: ').place(
			relx=.05, rely=.05, relwidth=.4, relheight=.1)
		sym = tk.Entry(top_win)
		sym.place(relx=.05, rely=.15, relwidth=.45, relheight=.1)

		tk.Button(top_win, text='Add >', command=add_sym).place(
			relx=.1, rely=.4, relwidth=.4, relheight=.1)
		tk.Button(top_win, text='Rem <').place(
			relx=.1, rely=.55, relwidth=.4, relheight=.1)

		sym_list = tk.Listbox(top_win)
		sym_list.place(relx=.55, rely=.05, relwidth=.4, relheight=.9)
		sym_list.bind('<<ListboxSelect>>', lambda e: print('Symbol'))

		for item in SYMBOLS:
			sym_list.insert(tk.END, item)

		top_win.mainloop()


if __name__ == '__main__':
	root = Window()
	root.mainloop()