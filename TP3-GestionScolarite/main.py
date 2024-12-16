import sys
import subprocess
import wx

class FenetreMenu(wx.Frame):
    def __init__(self, *args, **kw):
        super(FenetreMenu, self).__init__(*args, **kw)

        self.SetTitle("Gestion de Scolarité")
        self.SetSize(1000, 700)
        self.SetBackgroundColour('#FFFFFF')

        self.panel = wx.Panel(self)

        image = wx.Image("Icons/GS.png", wx.BITMAP_TYPE_PNG)
        image = image.Scale(self.GetSize().width, self.GetSize().height)  
        self.background_image = wx.Bitmap(image)
        self.sizer_principal = wx.BoxSizer(wx.VERTICAL)

        self.sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_accueil = wx.Button(self.panel, label="Accueil")
        self.btn_etudiant = wx.Button(self.panel, label="Gérer les Étudiants")
        self.btn_professeur = wx.Button(self.panel, label="Gérer les Professeurs")
        self.btn_module = wx.Button(self.panel, label="Gérer les Modules")
        self.btn_note = wx.Button(self.panel, label="Gérer les Notes")
        self.sizer_boutons.Add(self.btn_accueil, 0, wx.ALL, 5)
        self.sizer_boutons.Add(self.btn_etudiant, 0, wx.ALL, 5)
        self.sizer_boutons.Add(self.btn_professeur, 0, wx.ALL, 5)
        self.sizer_boutons.Add(self.btn_module, 0, wx.ALL, 5)
        self.sizer_boutons.Add(self.btn_note, 0, wx.ALL, 5)
        self.sizer_principal.Add(self.sizer_boutons, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)

        self.label_contenu = wx.StaticText(self.panel, label="Bienvenue dans l'application Gestion de Scolarité")
        self.label_contenu.SetForegroundColour('#cc0000')
        self.label_contenu.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.sizer_principal.Add(self.label_contenu, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        self.panel.SetSizer(self.sizer_principal)

        self.btn_accueil.Bind(wx.EVT_BUTTON, self.afficher_accueil)
        self.btn_etudiant.Bind(wx.EVT_BUTTON, self.afficher_etudiant)
        self.btn_professeur.Bind(wx.EVT_BUTTON, self.afficher_professeur)
        self.btn_module.Bind(wx.EVT_BUTTON, self.afficher_module)
        self.btn_note.Bind(wx.EVT_BUTTON, self.afficher_note)

        self.SetIcon(wx.Icon("Icons/iconUni.png"))

        self.panel.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        dc.DrawBitmap(self.background_image, 0, 0)

    def afficher_accueil(self, event):
        subprocess.Popen(["python", "main.py"])

    def afficher_professeur(self, event):
        subprocess.Popen(["python", "professeur.py"])

    def afficher_etudiant(self, event):
        subprocess.Popen(["python", "etudiant.py"])

    def afficher_module(self, event):
        subprocess.Popen(["python", "module.py"])

    def afficher_note(self, event):
        subprocess.Popen(["python", "note.py"])

if __name__ == "__main__":
    app = wx.App(False)
    window = FenetreMenu(None)
    window.Show()
    app.MainLoop()
