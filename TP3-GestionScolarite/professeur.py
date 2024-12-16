import sqlite3 
import wx

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Prof (
            id INTEGER,
            nom TEXT,
            prenom TEXT,
            immatriculation INTEGER PRIMARY KEY,
            departement TEXT
        )''')
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM Prof")
        return self.cursor.fetchall()

    def add_prof(self, prof_data):
        self.cursor.execute("INSERT INTO Prof (id, nom, prenom, immatriculation, departement) VALUES (?, ?, ?, ?, ?)", prof_data)
        self.conn.commit()

    def update_prof(self, immatriculation, new_data):
        self.cursor.execute("UPDATE Prof SET id = ?, nom = ?, prenom = ?, departement = ? WHERE immatriculation = ?", new_data + [immatriculation])
        self.conn.commit()

    def delete_prof(self, immatriculation):
        self.cursor.execute("DELETE FROM Prof WHERE immatriculation = ?", (immatriculation,))
        self.conn.commit()

    def find_by_immatriculation(self, immatriculation):
        self.cursor.execute("SELECT * FROM Prof WHERE immatriculation = ?", (immatriculation,))
        return self.cursor.fetchone()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Gestion des Professeurs", size=(700, 500))
        self.db = Database()
        self.SetIcon(wx.Icon(r"Icons\iconUni.png", wx.BITMAP_TYPE_PNG))
        self.init_ui()
        self.load_data()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add buttons before the table
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_add = wx.Button(panel, label="Ajouter")
        btn_modify = wx.Button(panel, label="Modifier")
        btn_delete = wx.Button(panel, label="Supprimer")
        
        # Apply background and text color to buttons
        btn_add.SetBackgroundColour(wx.Colour(0, 128, 0)) 
        btn_add.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        btn_modify.SetBackgroundColour(wx.Colour(255, 165, 0))
        btn_modify.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        btn_delete.SetBackgroundColour(wx.Colour(255, 0, 0)) 
        btn_delete.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        btn_modify.Bind(wx.EVT_BUTTON, self.on_modify)
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        
        hbox.Add(btn_add, 0, wx.ALL, 5)
        hbox.Add(btn_modify, 0, wx.ALL, 5)
        hbox.Add(btn_delete, 0, wx.ALL, 5)
        
        vbox.Add(hbox, 0, wx.ALIGN_CENTER)
        
        # List control with background color
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "ID", width=50)
        self.list_ctrl.InsertColumn(1, "Nom", width=150)
        self.list_ctrl.InsertColumn(2, "Prénom", width=150)
        self.list_ctrl.InsertColumn(3, "Immatriculation", width=150)
        self.list_ctrl.InsertColumn(4, "Département", width=150)

        # Apply color to the table
        self.list_ctrl.SetBackgroundColour('#f0f0f0')  # Light grey background
        
        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        
        panel.SetSizer(vbox)

    def load_data(self):
        self.list_ctrl.DeleteAllItems()
        for prof in self.db.fetch_all():
            self.list_ctrl.Append([str(field) for field in prof])

    def on_add(self, event):
        AddProfDialog(self).ShowModal()
        self.load_data()

    def on_modify(self, event):
        ModifyProfDialog(self).ShowModal()
        self.load_data()

    def on_delete(self, event):
        DeleteProfDialog(self).ShowModal()
        self.load_data()

class AddProfDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Ajouter un Professeur", size=(400, 400))
        self.db = parent.db
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label="ID"), 0, wx.ALL, 5)
        self.id_ctrl = wx.TextCtrl(panel)
        self.id_ctrl.SetHint("ID")
        vbox.Add(self.id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Nom"), 0, wx.ALL, 5)
        self.nom_ctrl = wx.TextCtrl(panel)
        self.nom_ctrl.SetHint("Nom")
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Prénom"), 0, wx.ALL, 5)
        self.prenom_ctrl = wx.TextCtrl(panel)
        self.prenom_ctrl.SetHint("Prénom")
        vbox.Add(self.prenom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Immatriculation"), 0, wx.ALL, 5)
        self.immatriculation_ctrl = wx.TextCtrl(panel)
        self.immatriculation_ctrl.SetHint("Immatriculation")
        vbox.Add(self.immatriculation_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        
        vbox.Add(wx.StaticText(panel, label="Département"), 0, wx.ALL, 5)
        self.departement_ctrl = wx.Choice(panel, choices=["Biologie", "Chimie", "Géologie", "Informatique", "Mathématiques", "Physique"])
        vbox.Add(self.departement_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Ajouter")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(0, 128, 0)) 
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255)) 
        panel.SetSizer(vbox)
    
    def on_save(self, event):
        data = (
            self.id_ctrl.GetValue(),
            self.nom_ctrl.GetValue(),
            self.prenom_ctrl.GetValue(),
            self.immatriculation_ctrl.GetValue(),
            self.departement_ctrl.GetString(self.departement_ctrl.GetSelection()) 
        )
        if all(data):
            self.db.add_prof(data)
            self.Close()
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)


class ModifyDetailsDialog(wx.Dialog):
    def __init__(self, parent, prof):
        super().__init__(parent, title="Modifier Détails du Professeur", size=(400, 400))
        self.db = parent.db
        self.immatriculation = prof[3]  

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label="ID"), 0, wx.ALL, 5)
        self.id_ctrl = wx.TextCtrl(panel, value=str(prof[0]))
        vbox.Add(self.id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Nom"), 0, wx.ALL, 5)
        self.nom_ctrl = wx.TextCtrl(panel, value=prof[1])
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Prénom"), 0, wx.ALL, 5)
        self.prenom_ctrl = wx.TextCtrl(panel, value=prof[2])
        vbox.Add(self.prenom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Département"), 0, wx.ALL, 5)
        self.departement_ctrl = wx.ComboBox(panel, choices=["Biologie", "Chimie", "Géologie", "Informatique", "Mathématiques", "Physique"],
                                          value=prof[4], style=wx.CB_READONLY)
        vbox.Add(self.departement_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Enregistrer les modifications")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(255, 165, 0))
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255))  # White text

        panel.SetSizer(vbox)

    def on_save(self, event):
        new_data = [
            self.id_ctrl.GetValue(),
            self.nom_ctrl.GetValue(),
            self.prenom_ctrl.GetValue(),
            self.departement_ctrl.GetString(self.departement_ctrl.GetSelection())
        ]
        if all(new_data):
            self.db.update_prof(self.immatriculation, new_data)
            self.Close()
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)


class ModifyProfDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Modifier un Professeur", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.immatriculation_ctrl = wx.TextCtrl(panel)
        self.immatriculation_ctrl.SetHint("Immatriculation")
        vbox.Add(self.immatriculation_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_find = wx.Button(panel, label="Rechercher")
        btn_find.Bind(wx.EVT_BUTTON, self.on_find)
        vbox.Add(btn_find, 0, wx.ALL | wx.CENTER, 5)
        btn_find.SetBackgroundColour("#2E2EFF") 
        btn_find.SetForegroundColour(wx.Colour(255, 255, 255)) 

        panel.SetSizer(vbox)

    def on_find(self, event):
        immatriculation = self.immatriculation_ctrl.GetValue()
        prof = self.db.find_by_immatriculation(immatriculation)
        if prof:
            ModifyDetailsDialog(self, prof).ShowModal()
            self.Close()
        else:
            wx.MessageBox("Professeur non trouvé", "Erreur", wx.OK | wx.ICON_ERROR)

class DeleteProfDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Supprimer un Professeur", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.immatriculation_ctrl = wx.TextCtrl(panel)
        self.immatriculation_ctrl.SetHint("Immatriculation")
        vbox.Add(self.immatriculation_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_delete = wx.Button(panel, label="Supprimer")
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        vbox.Add(btn_delete, 0, wx.ALL | wx.CENTER, 5)
        btn_delete.SetBackgroundColour(wx.Colour(255, 0, 0)) 
        btn_delete.SetForegroundColour(wx.Colour(255, 255, 255)) 

        panel.SetSizer(vbox)


    def on_delete(self, event):
        immatriculation = self.immatriculation_ctrl.GetValue()
        prof = self.db.find_by_immatriculation(immatriculation)
        if prof:
            nom_prof = prof[1] 
            prenom_prof = prof[2]  
            full_name = f"{nom_prof} {prenom_prof}"
            confirmation_message = f"Voulez-vous vraiment supprimer {full_name}?"
            
            if wx.MessageBox(confirmation_message, "Confirmation", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                self.db.delete_prof(immatriculation)
                self.Close()
        else:
            wx.MessageBox("Prof non trouvé", "Erreur", wx.OK | wx.ICON_ERROR)        

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
