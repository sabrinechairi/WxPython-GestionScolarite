import sqlite3
import wx


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Module (
            module_id INTEGER PRIMARY KEY,
            etudiant_num_apogee INTEGER,
            prof_matricule INTEGER,
            nom TEXT, 
            FOREIGN KEY (etudiant_num_apogee) REFERENCES Etudiant(num_apogee),
            FOREIGN KEY (prof_matricule) REFERENCES Prof(immatriculation)
        )''')
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM Module")
        return self.cursor.fetchall()

    def add_module(self, module_data):
        self.cursor.execute("INSERT INTO Module (etudiant_num_apogee, prof_matricule, nom) VALUES (?, ?, ?)",
                            module_data)
        self.conn.commit()

    def update_module(self, module_id, new_data):
        query = "UPDATE Module SET etudiant_num_apogee = ?, prof_matricule = ?, nom = ? WHERE module_id = ?"
        self.cursor.execute(query, new_data + (module_id,))
        self.conn.commit()

    def delete_module(self, module_id):
        self.cursor.execute("DELETE FROM Module WHERE module_id = ?", (module_id,))
        self.conn.commit()

    def find_by_module_id(self, module_id):
        self.cursor.execute("SELECT * FROM Module WHERE module_id = ?", (module_id,))
        return self.cursor.fetchone()

    def get_all_etudiants(self):
        self.cursor.execute("SELECT num_apogee FROM Etudiant")
        return [str(row[0]) for row in self.cursor.fetchall()]

    def get_all_profs(self):
        self.cursor.execute("SELECT immatriculation FROM Prof")
        return [str(row[0]) for row in self.cursor.fetchall()]


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Gestion des Modules", size=(700, 500))
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
        self.list_ctrl.InsertColumn(1, "Numéro Apogée Étudiant", width=150)
        self.list_ctrl.InsertColumn(2, "Matricule Professeur", width=150)
        self.list_ctrl.InsertColumn(3, "Nom du Module", width=150)

        # Apply color to the table
        self.list_ctrl.SetBackgroundColour('#f0f0f0')

        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)

    def load_data(self):
        self.list_ctrl.DeleteAllItems()
        for module in self.db.fetch_all():
            self.list_ctrl.Append([str(field) for field in module])

    def on_add(self, event):
        AddModuleDialog(self).ShowModal()
        self.load_data()

    def on_modify(self, event):
        ModifyModuleDialog(self).ShowModal()
        self.load_data()

    def on_delete(self, event):
        DeleteModuleDialog(self).ShowModal()
        self.load_data()


class AddModuleDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Ajouter un Module", size=(400, 400))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Récupérer les numéros d'apogée des étudiants et les matricules des professeurs
        self.etudiants = self.db.get_all_etudiants()
        self.profs = self.db.get_all_profs()

        vbox.Add(wx.StaticText(panel, label="ID du Module"), 0, wx.ALL, 5)
        self.nom_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Numéro Apogée Étudiant"), 0, wx.ALL, 5)
        self.etudiant_num_apogee_ctrl = wx.ComboBox(panel, choices=self.etudiants, style=wx.CB_READONLY)
        vbox.Add(self.etudiant_num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Matricule Professeur"), 0, wx.ALL, 5)
        self.prof_matricule_ctrl = wx.ComboBox(panel, choices=self.profs, style=wx.CB_READONLY)
        vbox.Add(self.prof_matricule_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Nom du Module"), 0, wx.ALL, 5)
        self.nom_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # Bouton pour sauvegarder
        btn_save = wx.Button(panel, label="Ajouter")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(0, 128, 0))
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255))

        panel.SetSizer(vbox)

    def on_save(self, event):

        selected_etudiant = self.etudiant_num_apogee_ctrl.GetValue()
        selected_prof = self.prof_matricule_ctrl.GetValue()
        if selected_etudiant and selected_prof: 
            data = (
                selected_etudiant,
                selected_prof,
                self.nom_ctrl.GetValue()
            )
            if all(data):
                self.db.add_module(data)
                self.Close()
            else:
                wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Veuillez sélectionner un étudiant et un professeur", "Erreur", wx.OK | wx.ICON_ERROR)


class ModifyModuleDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Modifier un Module", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.module_id_ctrl = wx.TextCtrl(panel)
        self.module_id_ctrl.SetHint("ID du Module")
        vbox.Add(self.module_id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_find = wx.Button(panel, label="Rechercher")
        btn_find.Bind(wx.EVT_BUTTON, self.on_find)
        vbox.Add(btn_find, 0, wx.ALL | wx.CENTER, 5)
        btn_find.SetBackgroundColour("#2E2EFF")
        btn_find.SetForegroundColour(wx.Colour(255, 255, 255))

        panel.SetSizer(vbox)

    def on_find(self, event):
        module_id = self.module_id_ctrl.GetValue()
        module = self.db.find_by_module_id(module_id)
        if module:
            ModifyDetailsModuleDialog(self, module).ShowModal()
            self.Close()
        else:
            wx.MessageBox("Module non trouvé", "Erreur", wx.OK | wx.ICON_ERROR)


class ModifyDetailsModuleDialog(wx.Dialog):
    def __init__(self, parent, module):
        super().__init__(parent, title="Modifier Détails du Module", size=(400, 400))
        self.db = parent.db
        self.module = module

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # ComboBox pour les Étudiants
        self.etudiants = self.db.get_all_etudiants()
        self.profs = self.db.get_all_profs()

        self.etudiant_num_apogee_ctrl = wx.ComboBox(panel, choices=self.etudiants, style=wx.CB_READONLY)
        self.etudiant_num_apogee_ctrl.SetValue(str(module[1]))
        vbox.Add(wx.StaticText(panel, label="Numéro Apogée Étudiant"), 0, wx.ALL, 5)
        vbox.Add(self.etudiant_num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.prof_matricule_ctrl = wx.ComboBox(panel, choices=self.profs, style=wx.CB_READONLY)
        self.prof_matricule_ctrl.SetValue(str(module[2]))
        vbox.Add(wx.StaticText(panel, label="Matricule Professeur"), 0, wx.ALL, 5)
        vbox.Add(self.prof_matricule_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.nom_ctrl = wx.TextCtrl(panel)
        self.nom_ctrl.SetValue(module[3])
        vbox.Add(wx.StaticText(panel, label="Nom du Module"), 0, wx.ALL, 5)
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Enregistrer")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(0, 128, 0))
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255))

        panel.SetSizer(vbox)

    def on_save(self, event):
        module_id = self.module[0]
        data = (
            self.etudiant_num_apogee_ctrl.GetValue(),
            self.prof_matricule_ctrl.GetValue(),
            self.nom_ctrl.GetValue()
        )
        if all(data):
            self.db.update_module(module_id, data)
            self.Close()
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)


class DeleteModuleDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Supprimer un Module", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.module_id_ctrl = wx.TextCtrl(panel)
        self.module_id_ctrl.SetHint("ID du Module")
        vbox.Add(self.module_id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_delete = wx.Button(panel, label="Supprimer")
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        vbox.Add(btn_delete, 0, wx.ALL | wx.CENTER, 5)
        btn_delete.SetBackgroundColour(wx.Colour(255, 0, 0))
        btn_delete.SetForegroundColour(wx.Colour(255, 255, 255))

        panel.SetSizer(vbox)


    def on_delete(self, event):
        module_id = self.module_id_ctrl.GetValue()
        module = self.db.find_by_module_id(module_id)
        if module:
            nom_module = module[3] 
            confirmation_message = f"Voulez-vous vraiment supprimer {nom_module}?"
            
            if wx.MessageBox(confirmation_message, "Confirmation", wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                self.db.delete_module(module_id)
                self.Close()
        else:
            wx.MessageBox("Module non trouvé", "Erreur", wx.OK | wx.ICON_ERROR)        


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
