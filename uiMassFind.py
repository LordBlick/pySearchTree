#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

'''
 This program source code file is part of pySearchTree, a text files search application.
 
 Copyright  © 2021 by LordBlick (at) gmail.com
 
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, you may find one here:
 http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
 or you may search the http://www.gnu.org website for the version 2 license,
 or you may write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
'''

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango, GLib

from os import path as ph
H = ph.expanduser('~') # Home dir
hh = lambda s: s.replace(H, '~')
from sys import stdout as sto
_p = lambda _str: sto.write(hh(str(_str)))
debug = (False, True)[1]
def _d(_str):
	if debug: _p(_str)

class searchTextView:
	def __init__(it, ui, mainWindow, textView):
		it.ui = ui
		it.dlgSrchPos = None
		it.mainWindow = mainWindow
		it.textView = textView
		dlg = it.dlgSrch = ui.bld.get_object('dlgSrch')
		dlg.Entry = ui.bld.get_object('eFind')
		dlg.Entry.connect("changed", it.searchFor, 'interactive')
		bp = ui.bld.get_object('bp')
		bp.connect("clicked", it.searchFor, 'backward')
		bn = ui.bld.get_object('bn')
		bn.connect("clicked", it.searchFor, 'forward')
		bOK = ui.bld.get_object('bOK')
		bOK.connect("clicked", lambda xargs: it.hideDlgSrch())
		dlg.found = None
		dlg.flags = Gtk.TextSearchFlags.TEXT_ONLY | Gtk.TextSearchFlags.VISIBLE_ONLY # CASE_INSENSITIVE
		#dlg.show_all()

	def showDlgSrch(it, widget):
		it.dlgSrch.present()
		dlg = it.dlgSrch
		if it.dlgSrchPos:
			dlg.move(*it.dlgSrchPos)
		txtBuff = it.textView.get_buffer()
		sel = txtBuff.get_selection_bounds()
		if sel:
			dlg.found = sel
			dlg.Entry.set_text(txtBuff.get_text(*sel))
		dlg.set_keep_above(True)

	def hideDlgSrch(it):
		dlg = it.dlgSrch
		if dlg and(dlg.get_property("visible")):
			it.dlgSrchPos = dlg.get_position()
			dlg.hide()

	def getFound(it, txtBuff, srchType, txtSrch):
		dlg = it.dlgSrch
		if it.textView.changed:
			print("skip")
			dlg.found = None
			it.textView.changed = False
		if dlg.found:
			if srchType in ('interactive', 'backward'):
				iterB = dlg.found[0]
			else:
				iterB = dlg.found[1]
		else:
			iterB = None
		if not(iterB):
			if srchType in ('interactive', 'forward'):
				iterB = txtBuff.get_start_iter()
			else:
				iterB = txtBuff.get_end_iter()
		if srchType in ('interactive', 'forward'):
			return iterB.forward_search(txtSrch, dlg.flags, None)
		else:
			return iterB.backward_search(txtSrch, dlg.flags, None)

	def searchFor(it, widget, srchType):
		dlg = it.dlgSrch
		txtSrch = dlg.Entry.get_text()
		if txtSrch:
			txtBuff = it.textView.get_buffer()
			lastfound = dlg.found
			found = dlg.found = it.getFound(txtBuff, srchType, txtSrch)
			if lastfound and(not(found)):
				found = dlg.found = it.getFound(txtBuff, srchType, txtSrch)
			if found:
				it.textView.scroll_to_iter (found[0], 0)
				txtBuff.select_range(*found)

circles = 8 # Warning: At least 2 circles…
rot_radius = 12
circle_radius_min = 1
circle_radius_max = 4
circle_radius_step = (circle_radius_max-circle_radius_min)/(circles-1)
import cairo
import math


class SpinnerDrawer():
	def __init__(it, drwArea):
		drwArea.__init__()
		it.drwArea = drwArea
		it.rot = 0
		drwArea.connect("draw", it.on_draw)
		it.refresh()

	def refresh(it):
		rect = it.drwArea.get_allocation()
		drw_wnd = it.drwArea.get_window()
		if drw_wnd:
			drw_wnd.invalidate_rect(rect, True)

	def tick(it):
		it.refresh()
		it.rot = round(it.rot+.1, 1)
		if it.rot>2*math.pi:
			it.rot = round(it.rot-2*math.pi, 1)
		return True

	def on_draw(it, w, event):
		drw_wnd = w.get_window()
		it.cr = drw_wnd.cairo_create()
		geom = drw_wnd.get_geometry()
		it.draw(geom.width, geom.height)

	def draw(it, width, height):
		cr = it.cr
		matrix = cairo.Matrix(1, 0, 0, 1, width/2, height/2)
		cr.transform(matrix) # Make it so...
		cr.save()
		ThingMatrix = cairo.Matrix(1, 0, 0, 1, 0, 0)
		cairo.Matrix.translate(ThingMatrix, 0, 0)
		cr.transform(ThingMatrix)
		cairo.Matrix.rotate(ThingMatrix, it.rot)
		cr.transform(ThingMatrix)
		it.drawSpinner(cr)
		cr.restore()

	def drawSpinner(it, cr):
		angle_step = 2*math.pi/circles
		for idx in reversed(range(circles)):
			circle_data = math.sin(idx*angle_step)*rot_radius, math.cos(idx*angle_step)*rot_radius,\
				circle_radius_max-circle_radius_step*idx, 0, 2*math.pi
			cr.arc(*circle_data)
			cr.set_source_rgb(idx/(circles-1), 1-idx/(circles-1), .0)
			cr.fill()
			cr.set_line_width(0.8)
			cr.arc(*circle_data)
			cr.set_source_rgb(1, 1, 1)
			cr.stroke()

act_set = lambda s: set(s.split())
ui_actions  = act_set('LogClear FindPhraseIco')
actions  = act_set('Find FindBreak SrchLog Quit')
switches = act_set('ChangeFileset ChangeRoot SrchInfo MaskHome')
widgets = act_set('mainWindow accMain logView labFileset lsFileset '\
			'rendFileset cbFileset drwSpinner toggRoot '\
			'toggMaskHome toggSrchInfo labFindPhrase txtFindPhrase')

class massFindUI:
	def __init__(ui):
		ui.Init()
		if __name__ == "__main__":
			ui.mainWindow.connect("destroy", lambda w: ui.Quit())
			ui.buttQuit.connect("clicked", lambda w: ui.Quit())
			ui.buttClear.connect("clicked", ui.go_LogClear)
			ui.buttSearchLog.connect("clicked", ui.stv.showDlgSrch)
			ui._p("User Interface Test...\n")
			ui.uiEnter()

	Enter = lambda ui: Gtk.main()
	Quit  = lambda ui: Gtk.main_quit()
	bt_id = lambda ui, base_id: f"butt{base_id}"

	def Init(ui):
		rp = ui.runpath = ph.dirname(ph.realpath(__file__))
		if __name__ == "__main__":
			ui.cfg = {}

		ui.bld = Gtk.Builder()
		ui.bld.add_from_file(ph.join(ph.dirname(ph.abspath(__file__)), 'ui', 'pySearchTree.ui'))
		for action in actions:
			bt_id = ui.bt_id(action)
			setattr(ui, bt_id, ui.bld.get_object(bt_id))
		for wg_id in widgets:
			setattr(ui, wg_id, ui.bld.get_object(wg_id))

		geo = Gdk.Geometry()
		geo.min_width, geo.min_width = 510, 350
		ui.mainWindow.set_geometry_hints(None, geo, Gdk.WindowHints.MIN_SIZE)
		ui.mainWindow.show_all()
		ui.mainWindow.set_keep_above(True)
		ui.mainWindow.present()

		lv = ui.logView
		lv.set_text = lambda txt: lv.get_buffer().set_text(txt)
		lv.clear_text = lambda: lv.set_text('')

		global _l, _lp
		_l, _lp = ui._p, ui._lp

		ui.stv = searchTextView(ui, ui.mainWindow, ui.logView)
		ui.drs = SpinnerDrawer(ui.drwSpinner)
		ui.drwSpinner.set_size_request(48, 48)

	def createTxtTags(ui):
		lb = ui.logView.get_buffer()
		_B = Pango.Weight.BOLD
		ui.tgFlNm = lb.create_tag('fnm', weight = _B)
		ui.tgPhrs = lb.create_tag('phr', weight = _B)
		ui.tg_Err = lb.create_tag('err', weight = _B)
		ui.tgWarn = lb.create_tag('wrn', weight = _B)
		ui.tgEnum = lb.create_tag('num', weight = _B)

	def Connections(ui):
		handlers = {}
		for hn in (dr[3:] for dr in dir(ui) if dr[:3]=='go_'):
			handlers[f"ui_{hn}"] = getattr(ui, f"go_{hn}")
		return handlers

	def go_LogClear(ui, w):
		ui.logView.clear_text()

	def go_PhraseIcons(ui, ed, icoPos, sigEvent):
		if icoPos == Gtk.EntryIconPosition.SECONDARY:
			ed.set_text('')

	def _p(ui, txt, tag=None, short_path=False):
		buff = ui.logView.get_buffer()
		end = buff.get_end_iter()
		text = hh(txt) if short_path else txt
		if tag and(isinstance(tag, str)):
			tagTab = buff.get_tag_table()
			tagByNm = tagTab.lookup(tag)
			if tagByNm:
				tag = tagByNm
			elif hasattr(ui, tag):
				tag = getattr(ui, tag)
			else:
				tag = None
		if not(isinstance(tag, Gtk.TextTag)):
			buff.insert(end, text)
			return
		buff.insert_with_tags(end, text, tag)

	#TODO: Add scroll to end
	def _lp(ui, ls_txt, short_path=True):
		for idx, txt_obj in enumerate(ls_txt):
			if isinstance(txt_obj, str):
				ui._p(txt_obj, short_path=short_path)
			elif isinstance(txt_obj, tuple) and len(txt_obj)==2:
				ui._p(txt_obj[0], tag=txt_obj[1], short_path=short_path)
			else:
				raise TypeError(f"Unknown format in {ls_txt}[{idx}]")

	def getWinGeometry(ui, win):
		pos = win.get_position()
		size = win.get_size()
		return pos.root_x, pos.root_y, size.width, size.height

	def getTxtWinGeometry(ui, win):
		geo = ui.getWinGeometry(win)
		txtGeo = ','.join(f"{i:d}" for i in geo)
		dlgName = win.get_title()
		_d(f"Current Window „{dlgName}” geometry: {txtGeo}\n")
		return txtGeo

	def setWinGeometry_timed(ui, win, geo):
		_d(f"Repositioning Window: „{win.get_title()}” to:\n")
		_d(f"pos: x:{geo[0]}, y:{ geo[1]}\n")
		_d(f"size: w:{geo[2]}, h:{geo[3]}\n")
		gdw = win.get_window()
		gdw.move_resize(*geo)
		return False # run only once

	def setWinGeometry(ui, win, geo):
		GLib.idle_add(ui.setWinGeometry_timed, win, geo)

	def setTxtWinGeometry(ui, win, txtGeo):
		geo = tuple(map(int, txtGeo.split(',')))
		if len(geo)==4:
			ui.setWinGeometry(win, geo)
		else:
			_d(f"Strange geo situation:{geo}\n")

	#TODO: use Glade dialog included already in UI file
	def dialogChooseFile(ui, parent=None, startDir=None, startFile=None, filters=None, title='Select a file...', act='file_open', bShowHidden=False):
		action = {
			'file_open': Gtk.FileChooserAction.OPEN,
			'file_save': Gtk.FileChooserAction.SAVE,
			'dir_open': Gtk.FileChooserAction.SELECT_FOLDER,
			'dir_create': Gtk.FileChooserAction.CREATE_FOLDER,
			}[act]
		hDialog = Gtk.FileChooserDialog(title=title, parent=parent, action=action,
			buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK) )
		if filters:
			for fnFilter in filters:
				hDialog.add_filter(fnFilter)
			allFilter = Gtk.FileFilter()
			allFilter.set_name("All files (*.*)")
			allFilter.add_pattern("*")
			hDialog.add_filter(allFilter)
		hDialog.set_default_response(Gtk.ResponseType.OK)
		hDialog.set_show_hidden(bShowHidden)
		if startDir:
			hDialog.set_current_folder(startDir)
		if startFile:
			if act=='file_save':
				hDialog.set_current_name(startFile)
			elif act=='file_open':
				hDialog.set_filename(startFile)
		respFileName = hDialog.run()
		fileName = None
		if respFileName==Gtk.ResponseType.OK:
			fileName = hDialog.get_filename()
		hDialog.destroy()
		return fileName

# Entry point
if __name__ == "__main__":
	massFindUI()
