#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- tabstop: 4 -*-

'''
 This program source code file is part of pySearchTree, a text files search
 application.
 
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

import gtk, pango

Height = 30

def getTxtPixelWidth(widget, txt, fontDesc=None):
	pangoLayout = widget.create_pango_layout(txt)
	if fontDesc:
		pangoLayout.set_font_description(fontDesc)
	pangoTxtSpc = pangoLayout.get_pixel_size()[0]
	del(pangoLayout)
	return pangoTxtSpc

def npLabel(txtLabel, fontDesc=None, xalign=None, selectable=False):
	hLabel = gtk.Label(txtLabel)
	if fontDesc:
		hLabel.modify_font(fontDesc)
	if type(xalign)==float and(0.<=xalign<=1.):
		yalign = hLabel.get_alignment()[1]
		hLabel.set_alignment(xalign, yalign)
	if type(selectable)==bool:
		hLabel.set_selectable(selectable)
	hLabel.show()
	return hLabel

def Label(txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None, xalign=None, selectable=False):
	hLabel = npLabel(txtLabel, fontDesc=fontDesc, xalign=xalign, selectable=selectable)
	if not height:
		height=Height
	hLabel.set_size_request(width, height)
	if hFixed:
		hFixed.put(hLabel, posX, posY)
	return hLabel

def npButt(txtLabel, fileImage=None, stockID=None, fontDesc=None):
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
	return hButt

def Butt(txtLabel, hFixed, posX, posY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
	"""If stockID is set, txtLabel set as True means full stock button,
	non-null string - own Label for stock image,
	in other case - button with only stock image"""
	hButt = npButt(txtLabel, fileImage=fileImage, stockID=stockID, fontDesc=fontDesc)
	if not height:
		height = Height
	hButt.set_size_request(width, height)
	hFixed.put(hButt, posX, posY)
	return hButt

def Check(txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None):
	hCheck = gtk.CheckButton(label=txtLabel, use_underline=False)
	hLabel=hCheck.child
	if not height:
		height = Height
	hCheck.set_size_request(width, height)
	hFixed.put(hCheck, posX, posY)
	return hCheck

def entryIcoClr(ed, icoPos, sigEvent):
	if icoPos == gtk.ENTRY_ICON_SECONDARY:
		ed.set_text('')

def npEntry(startIco=None, clearIco=False, bEditable=True, fontDesc=None):
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
	return hEntry

def Entry(hFixed, posX, posY, width, height=None, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
	hEntry = npEntry(clearIco=clearIco, bEditable=bEditable, fontDesc=fontDesc)
	if not height:
		height = Height
	hEntry.set_size_request(width, height)
	hFixed.put(hEntry, posX, posY)
	return hEntry

def ComboBox(modelCb, hFixed, posX, posY, width, height=None, fontDesc=None, wrap=None, selTxt=0):
	if not height:
		height=Height
	hCb = gtk.ComboBox()
	cellRendr = gtk.CellRendererText()
	if fontDesc:
		cellRendr.set_property('font-desc', fontDesc)
	hCb.pack_start(cellRendr)
	hCb.set_attributes(cellRendr, text=selTxt)
	if wrap:
		hCb.set_wrap_width(wrap)
	else:
		cellRendr.set_property('ellipsize', pango.ELLIPSIZE_END)
	hCb.set_model(modelCb)
	hCb.set_size_request(width, height+4)
	hFixed.put(hCb, posX, posY-2)
	return hCb

def Toggle(txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None):
	hToggle = gtk.ToggleButton(label=txtLabel, use_underline=False)
	if fontDesc:
		hLabel = hToggle.child
		hLabel.modify_font(fontDesc)
	if not height:
		height=Height
	hToggle.set_size_request(width, height)
	hFixed.put(hToggle, posX, posY)
	return hToggle

class EasyTextView(gtk.TextView):
	def __init__(it):
		super(gtk.TextView, it).__init__()
		it.autoscroll = True
		it.changed = False

	def set_text(it, txt):
		it.get_buffer().set_text(txt)
		it.changed = True

	clear_text = lambda it: it.set_text('')

	def set_size_request(it, x, y):
		try:
			parent = it.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			parent.set_size_request(x, y)
		else:
			super(gtk.TextView, it).set_size_request(x, y)

	def get_text(it):
		tBuff = it.get_buffer()
		return tBuff.get_text(tBuff.get_start_iter(), tBuff.get_end_iter())
	
	def insert_end(it, txt, tag=None):
		buff = it.get_buffer()
		end = buff.get_end_iter()
		text = txt.encode('utf-8', errors='replace')
		if tag:
			buff.insert_with_tags(end, text, tag)
		else:
			buff.insert(end, text)
		del(end)
		it.changed = True

	def reScrollV(it, adjV, scrollV):
		"""Scroll to the bottom of the TextView when the adjustment changes."""
		if it.autoscroll:
			adjV.set_value(adjV.upper - adjV.page_size)
			scrollV.set_vadjustment(adjV)
		return

	def setTabSpace(it, spaces, fontDesc=None):
		pangoTabSpc = getTxtPixelWidth(it, ' '*spaces, fontDesc)
		tabArray =  pango.TabArray(1, True)
		tabArray.set_tab(0, pango.TAB_LEFT, pangoTabSpc)
		it.set_tabs(tabArray)
		return pangoTabSpc

def TextView(hFixed, posX, posY, width, height, bWrap=False, bEditable=True, tabSpace=2, fontDesc=None):
	hTextView = EasyTextView()
	hTextView.set_property("editable", bEditable)
	if fontDesc:
		hTextView.modify_font(fontDesc)
		hTextView.setTabSpace(tabSpace, fontDesc=fontDesc)
	if bWrap:
		hTextView.set_wrap_mode(gtk.WRAP_WORD)
	scrollViewTxt = gtk.ScrolledWindow()
	vadj = scrollViewTxt.get_vadjustment()
	vadj.connect('changed', hTextView.reScrollV, scrollViewTxt)
	scrollViewTxt.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	scrollViewTxt.add(hTextView)
	scrollViewTxt.set_size_request(width, height)
	hFixed.put(scrollViewTxt, posX, posY)
	return hTextView

def dialogChooseFile(parent=None, startDir=None, startFile=None, filters=None, title='Select a file...', act='file_open', bShowHidden=False):
	action = {
		'file_open': gtk.FILE_CHOOSER_ACTION_OPEN,
		'file_save': gtk.FILE_CHOOSER_ACTION_SAVE,
		'dir_open': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
		'dir_create': gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
		}[act]
	hDialog = gtk.FileChooserDialog(title=title, parent=parent, action=action,
		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
	if filters:
		for fnFilter in filters:
			hDialog.add_filter(fnFilter)
		allFilter = gtk.FileFilter()
		allFilter.set_name("All files (*.*)")
		allFilter.add_pattern("*")
		hDialog.add_filter(allFilter)
	hDialog.set_default_response(gtk.RESPONSE_OK)
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
	if respFileName==gtk.RESPONSE_OK:
		fileName = hDialog.get_filename()
	hDialog.destroy()
	return fileName
