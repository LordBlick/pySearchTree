#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

'''
 This program source code file is shared library for easy pygtk+2 TextView widget
searching.
 
 Copyright  © 2015 by LordBlick (at) gmail.com
 
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

import gtk
Height = 20

def Label(txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None, xalign=None, selectable=False):
	hLabel = gtk.Label(txtLabel)
	if fontDesc:
		hLabel.modify_font(fontDesc)
	if type(xalign)==float and(0.<=xalign<=1.):
		yalign = hLabel.get_alignment()[1]
		hLabel.set_alignment(xalign, yalign)
	if type(selectable)==bool:
		hLabel.set_selectable(selectable)
	hLabel.show()
	if not height:
		height=Height
	hLabel.set_size_request(width, height)
	if hFixed:
		hFixed.put(hLabel, posX, posY)
	return hLabel

def Butt(txtLabel, hFixed, posX, posY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
	"""If stockID is set, txtLabel set as True means full stock button,
	non-null string - own Label for stock image,
	in other case - button with only stock image"""
	if stockID == None and fileImage == None:
		hButt = gtk.Button(label=txtLabel, use_underline=False)
		if fontDesc:
			hLabel = hButt.child
			hLabel.modify_font(fontDesc)
	else:
		if type(txtLabel)==int or type(txtLabel)==float or type(txtLabel)==type(None) or (type(txtLabel)==str and txtLabel==''):
			txtLabel = bool(txtLabel)
		if type(txtLabel)==bool and txtLabel==True or type(txtLabel)==str:
			if stockID:
				hButt = gtk.Button(stock=stockID)
			elif fileImage:
				image = gtk.Image()
				image.set_from_file(fileImage)
				hButt = gtk.Button()
				hButt.add(image)
			if type(txtLabel)==str:
				hLabel = hButt.get_children()[0].get_children()[0].get_children()[1]
				hLabel.set_text(txtLabel)
				if fontDesc:
					hLabel.modify_font(fontDesc)
		else:
			image = gtk.Image()
			if stockID:
				image.set_from_stock(stockID, gtk.ICON_SIZE_BUTTON)
			elif fileImage:
				image.set_from_file(fileImage)
			hButt = gtk.Button()
			hButt.add(image)
	if not height:
		height = Height
	hButt.set_size_request(width, height)
	hFixed.put(hButt, posX, posY)
	return hButt

def entryIcoClr(ed, icoPos, sigEvent):
	if icoPos == gtk.ENTRY_ICON_SECONDARY:
		ed.set_text('')

def Entry(hFixed, posX, posY, width, height=None, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
	hEntry = gtk.Entry()
	if fontDesc:
		hEntry.modify_font(fontDesc)
	if startIco:
		textInput.set_icon_from_pixbuf(0, startIco)
	if clearIco:
		hEntry.set_icon_from_stock(1, gtk.STOCK_CLOSE)
		hEntry.set_icon_tooltip_text (1, 'Clear')
		hEntry.connect("icon-release", entryIcoClr)
	hEntry.set_property("editable", bool(bEditable))
	if not height:
		height = Height
	hEntry.set_size_request(width, height)
	hFixed.put(hEntry, posX, posY)
	return hEntry

class searchTextView:
	def __init__(it, ui, mainWindow, textView):
		it.ui = ui
		it.mainWindow = mainWindow
		it.textView = textView
		it.dlgSrch = it.dlgSrchPos = None

	def dialogFind(it):
		dlg = it.dlgSrch = gtk.Window(gtk.WINDOW_TOPLEVEL)
		if hasattr(it.ui, 'accGroup'):
			dlg.add_accel_group(it.ui.accGroup)
		dlg.set_border_width(5)
		dlg.set_resizable(False)
		dlg.set_title('Find')
		dlg.set_transient_for(it.mainWindow)
		dlg.set_destroy_with_parent(True)
		dlg.set_deletable(False)
		dlg.set_skip_taskbar_hint(False)
		# # # # # # # # # # # # # # # # # # # # # # # # #
		dlgFrame = gtk.Fixed()

		Label("Please enter phrase to find:", dlgFrame, 0, 0, 150)
		dlg.Entry = Entry(dlgFrame, 0, 25, 200, clearIco=True)
		dlg.Entry.connect("changed", it.searchFor, 'interactive')
		bp = dlg.buttonPrev = Butt("Previous", dlgFrame, 0, 50, 70, stockID=gtk.STOCK_GO_BACK)
		bp.connect("clicked", it.searchFor, 'backward')
		bn = dlg.buttonNext = Butt("Next", dlgFrame, 75, 50, 70, stockID=gtk.STOCK_GO_FORWARD)
		bn.connect("clicked", it.searchFor, 'forward')
		hButtonOK = Butt("OK", dlgFrame, 170, 50, 30)
		hButtonOK.connect("clicked", lambda xargs: it.hideDlgSrch())
		dlg.found = None
		dlg.flags = gtk.TEXT_SEARCH_TEXT_ONLY | gtk.TEXT_SEARCH_VISIBLE_ONLY

		dlg.add(dlgFrame)
		dlg.show_all()

	def showDlgSrch(it, widget):
		if it.dlgSrch:
			it.dlgSrch.present()
		else:
			it.dialogFind()
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
