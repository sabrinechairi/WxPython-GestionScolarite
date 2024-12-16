import sqlite3
import wx

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        # Create Etudiant table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Etudiant (
            id INTEGER,
            nom TEXT,
            prenom TEXT,
            num_apogee INTEGER PRIMARY KEY,
            master TEXT
        )''')
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM Etudiant")
        return self.cursor.fetchall()

    def add_etudiant(self, etudiant_data):
        self.cursor.execute("INSERT INTO Etudiant (id, nom, prenom, num_apogee, master) VALUES (?, ?, ?, ?, ?)", etudiant_data)
        self.conn.commit()

    def update_etudiant(self, num_apogee, new_data):
        self.cursor.execute("UPDATE Etudiant SET id = ?, nom = ?, prenom = ?, master = ? WHERE num_apogee = ?", new_data + [num_apogee])
        self.conn.commit()

    def delete_etudiant(self, num_apogee):
        self.cursor.execute("DELETE FROM Etudiant WHERE num_apogee = ?", (num_apogee,))
        self.conn.commit()

    def find_by_num_apogee(self, num_apogee):
        self.cursor.execute("SELECT * FROM Etudiant WHERE num_apogee = ?", (num_apogee,))
        return self.cursor.fetchone()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Gestion des Etudiants", size=(700, 500))
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
        btn_add.SetForegroundColour(wx.Colour(255, 255, 255))  
        btn_modify.SetBackgroundColour(wx.Colour(255, 165, 0))
        btn_modify.SetForegroundColour(wx.Colour(255, 255, 255))  
        btn_delete.SetBackgroundColour(wx.Colour(255, 0, 0)) 
        btn_delete.SetForegroundColour(wx.Colour(255, 255, 255))  

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
        self.list_ctrl.InsertColumn(3, "Numéro d'Apogée", width=150)
        self.list_ctrl.InsertColumn(4, "Master", width=150)

        # Apply color to the table
        self.list_ctrl.SetBackgroundColour('#f0f0f0')  
        
        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        
        panel.SetSizer(vbox)

    def load_data(self):
        self.list_ctrl.DeleteAllItems()
        for etudiant in self.db.fetch_all():
            self.list_ctrl.Append([str(field) for field in etudiant])

    def on_add(self, event):
        AddEtudiantDialog(self).ShowModal()
        self.load_data()

    def on_modify(self, event):
        ModifyEtudiantDialog(self).ShowModal()
        self.load_data()

    def on_delete(self, event):
        DeleteEtudiantDialog(self).ShowModal()
        self.load_data()

class AddEtudiantDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Ajouter un Etudiant", size=(400, 400))
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

        vbox.Add(wx.StaticText(panel, label="Numéro d'Apogée"), 0, wx.ALL, 5)
        self.num_apogee_ctrl = wx.TextCtrl(panel)
        self.num_apogee_ctrl.SetHint("Numéro d'Apogée")
        vbox.Add(self.num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        
        vbox.Add(wx.StaticText(panel, label="Master"), 0, wx.ALL, 5)
        self.master_ctrl = wx.Choice(panel, choices=["B2S", "MQSE", "MRF", "MLAI",
                                                       "CARA", "IBGE", "MM", "GPM",
                                                       "MQL", "M2I", "MGEER"])
        vbox.Add(self.master_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Ajouter")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(0, 128, 0)) 
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255))  # White text

        panel.SetSizer(vbox)
    
    def on_save(self, event):
        data = (
            self.id_ctrl.GetValue(),
            self.nom_ctrl.GetValue(),
            self.prenom_ctrl.GetValue(),
            self.num_apogee_ctrl.GetValue(),
            self.master_ctrl.GetString(self.master_ctrl.GetSelection()) 
        )
        if all(data):
            self.db.add_etudiant(data)
            self.Close()
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)


class ModifyEtudiantDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Modifier un Etudiant", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.num_apogee_ctrl = wx.TextCtrl(panel)
        self.num_apogee_ctrl.SetHint("Numéro d'Apogée")
        vbox.Add(self.num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_find = wx.Button(panel, label="Rechercher")
        btn_find.Bind(wx.EVT_BUTTON, self.on_find)
        vbox.Add(btn_find, 0, wx.ALL | wx.CENTER, 5)
        btn_find.SetBackgroundColour("#2E2EFF") 
        btn_find.SetForegroundColour(wx.Colour(255, 255, 255))  # White text

        panel.SetSizer(vbox)

    def on_find(self, event):
        num_apogee = self.num_apogee_ctrl.GetValue()
        etudiant = self.db.find_by_num_apogee(num_apogee)
        if etudiant:
            ModifyDetailsEtudiantDialog(self, etudiant).ShowModal()
            self.Close()
        else:
            wx.MessageBox("Etudiant non trouvé", "Erreur", wx.OK | wx.ICON_ERROR)

class ModifyDetailsEtudiantDialog(wx.Dialog):
    def __init__(self, parent, etudiant):
        super().__init__(parent, title="Modifier Détails de l'Etudiant", size=(400, 400))
        self.db = parent.db
        self.num_apogee = etudiant[3] 

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label="ID"), 0, wx.ALL, 5)
        self.id_ctrl = wx.TextCtrl(panel, value=str(etudiant[0]))
        vbox.Add(self.id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Nom"), 0, wx.ALL, 5)
        self.nom_ctrl = wx.TextCtrl(panel, value=etudiant[1])
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Prénom"), 0, wx.ALL, 5)
        self.prenom_ctrl = wx.TextCtrl(panel, value=etudiant[2])
        vbox.Add(self.prenom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Master"), 0, wx.ALL, 5)
        self.master_ctrl = wx.ComboBox(panel, choices=["B2S", "MQSE", "MRF", "MLAI",
                                                       "CARA", "IBGE", "MM", "GPM",
                                                       "MQL", "M2I", "MGEER"],
                                       value=etudiant[4], style=wx.CB_READONLY)
        vbox.Add(self.master_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Enregistrer les modifications")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(255, 165, 0))
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255)) 

        panel.SetSizer(vbox)

    def on_save(self, event):
        new_data = [
            self.id_ctrl.GetValue(),
            self.nom_ctrl.GetValue(),
            self.prenom_ctrl.GetValue(),
            self.master_ctrl.GetString(self.master_ctrl.GetSelection())
        ]
        if all(new_data):
            self.db.update_etudiant(self.num_apogee, new_data)
            self.Close()
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)

class DeleteEtudiantDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Supprimer un Etudiant", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.num_apogee_ctrl = wx.TextCtrl(panel)
        self.num_apogee_ctrl.SetHint("Numéro d'Apogée")
        vbox.Add(self.num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_delete = wx.Button(panel, label="Supprimer")
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        vbox.Add(btn_delete, 0, wx.ALL | wx.CENTER, 5)
        btn_delete.SetBackgroundColour(wx.Colour(255, 0, 0)) 
        btn_delete.SetForegroundColour(wx.Colour(255, 255, 255))  

        panel.SetSizer(vbox)

    def on_delete(self, event):
        num_apogee = self.num_apogee_ctrl.GetValue()
        etudiant = self.db.find_by_num_apogee(num_apogee)
        if etudiant:
            nom_etudiant = etudiant[1]  
            prenom_etudiant = etudiant[2] 
            full_name = f"{prenom_etudiant} {nom_etudiant}"
            confirmation_message = f"Voulez-vous vraiment supprimer {full_name}?"
            
            if wx.MessageBox(confirmation_message, "Confirmation", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                self.db.delete_etudiant(num_apogee)
                self.Close()
        else:
            wx.MessageBox("Etudiant non trouvé", "Erreur", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
