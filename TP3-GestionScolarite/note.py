import sqlite3
import wx


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("scolarite.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Note (
            id INTEGER PRIMARY KEY,
            etudiant_num_apogee INTEGER,
            module_id INTEGER,
            note REAL,
            FOREIGN KEY (etudiant_num_apogee) REFERENCES Etudiant(num_apogee),
            FOREIGN KEY (module_id) REFERENCES Module(module_id)
        )''')
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM Note")
        return self.cursor.fetchall()

    def add_note(self, note_data):
        self.cursor.execute("INSERT INTO Note (etudiant_num_apogee, module_id, note) VALUES (?, ?, ?)", note_data)
        self.conn.commit()

    def update_note(self, note_id, new_data):
        query = "UPDATE Note SET etudiant_num_apogee = ?, module_id = ?, note = ? WHERE id = ?"
        self.cursor.execute(query, new_data + (note_id,))
        self.conn.commit()

    def delete_note(self, note_id):
        self.cursor.execute("DELETE FROM Note WHERE id = ?", (note_id,))
        self.conn.commit()

    def find_by_note_id(self, note_id):
        self.cursor.execute("SELECT * FROM Note WHERE id = ?", (note_id,))
        return self.cursor.fetchone()

    def get_all_etudiants(self):
        self.cursor.execute("SELECT num_apogee FROM Etudiant")
        return [str(row[0]) for row in self.cursor.fetchall()]

    def get_all_modules(self):
        self.cursor.execute("SELECT module_id FROM Module")
        return [str(row[0]) for row in self.cursor.fetchall()]
    
    def find_by_num_apogee_and_module(self, num_apogee, module_id):
        self.cursor.execute("SELECT * FROM Note WHERE etudiant_num_apogee = ? AND module_id = ?", (num_apogee, module_id))
        return self.cursor.fetchone()


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Gestion des Notes", size=(700, 500))
        self.db = Database()
        self.SetIcon(wx.Icon(r"Icons\iconUni.png", wx.BITMAP_TYPE_PNG))
        self.init_ui()
        self.load_data()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        btn_add = wx.Button(panel, label="Ajouter")
        btn_modify = wx.Button(panel, label="Modifier")
        btn_delete = wx.Button(panel, label="Supprimer")

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

        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "ID", width=50)
        self.list_ctrl.InsertColumn(1, "Numéro Apogée Étudiant", width=150)
        self.list_ctrl.InsertColumn(2, "ID Module", width=150)
        self.list_ctrl.InsertColumn(3, "Note", width=150)

        self.list_ctrl.SetBackgroundColour('#f0f0f0')

        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)

    def load_data(self):
        self.list_ctrl.DeleteAllItems()
        for note in self.db.fetch_all():
            self.list_ctrl.Append([str(field) for field in note])

    def on_add(self, event):
        AddNoteDialog(self).ShowModal()
        self.load_data()

    def on_modify(self, event):
        ModifyNoteDialog(self).ShowModal()
        self.load_data()

    def on_delete(self, event):
        DeleteNoteDialog(self).ShowModal()
        self.load_data()


class AddNoteDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Ajouter une Note", size=(400, 400))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.etudiants = self.db.get_all_etudiants()
        self.modules = self.db.get_all_modules()

        vbox.Add(wx.StaticText(panel, label="ID de la Note"), 0, wx.ALL, 5)
        self.nom_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.nom_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Numéro Apogée Étudiant"), 0, wx.ALL, 5)
        self.etudiant_num_apogee_ctrl = wx.ComboBox(panel, choices=self.etudiants, style=wx.CB_READONLY)
        vbox.Add(self.etudiant_num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="ID Module"), 0, wx.ALL, 5)
        self.module_id_ctrl = wx.ComboBox(panel, choices=self.modules, style=wx.CB_READONLY)
        vbox.Add(self.module_id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(wx.StaticText(panel, label="Note"), 0, wx.ALL, 5)
        self.note_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.note_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Ajouter")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(0, 128, 0))
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255))

        panel.SetSizer(vbox)

    def on_save(self, event):
        etudiant_num_apogee = self.etudiant_num_apogee_ctrl.GetValue()
        module_id = self.module_id_ctrl.GetValue()
        note = self.note_ctrl.GetValue()

        if etudiant_num_apogee and module_id and note:
            self.db.add_note((etudiant_num_apogee, module_id, float(note)))
            self.EndModal(wx.ID_OK)


class ModifyNoteDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Modifier une Note", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Fields for searching by num_apogee and module_id
        self.etudiant_num_apogee_ctrl = wx.TextCtrl(panel)
        self.etudiant_num_apogee_ctrl.SetHint("Numéro Apogée Étudiant")
        vbox.Add(self.etudiant_num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

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
        num_apogee = self.etudiant_num_apogee_ctrl.GetValue()
        module_id = self.module_id_ctrl.GetValue()

        if num_apogee and module_id:
            self.note = self.db.find_by_num_apogee_and_module(num_apogee, module_id)
            if self.note:
                ModifyDetailsNoteDialog(self, self.note).ShowModal()
                self.Close()
            else:
                wx.MessageBox("Aucune note trouvée pour ces critères", "Erreur", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)



class ModifyDetailsNoteDialog(wx.Dialog):
    def __init__(self, parent, note):
        super().__init__(parent, title="Modifier Détails de la Note", size=(400, 400))
        self.db = parent.db
        self.note = note

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # ComboBox pour les Étudiants
        self.etudiants = self.db.get_all_etudiants()
        self.modules = self.db.get_all_modules()

        self.etudiant_num_apogee_ctrl = wx.ComboBox(panel, choices=self.etudiants, style=wx.CB_READONLY)
        self.etudiant_num_apogee_ctrl.SetValue(str(note[1]))  # Note -> Etudiant Numéro Apogée
        vbox.Add(wx.StaticText(panel, label="Numéro Apogée Étudiant"), 0, wx.ALL, 5)
        vbox.Add(self.etudiant_num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.module_id_ctrl = wx.ComboBox(panel, choices=self.modules, style=wx.CB_READONLY)
        self.module_id_ctrl.SetValue(str(note[2]))  # Note -> Module ID
        vbox.Add(wx.StaticText(panel, label="ID du Module"), 0, wx.ALL, 5)
        vbox.Add(self.module_id_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.note_ctrl = wx.TextCtrl(panel)
        self.note_ctrl.SetValue(str(note[3]))  # Note -> Valeur de la note
        vbox.Add(wx.StaticText(panel, label="Note"), 0, wx.ALL, 5)
        vbox.Add(self.note_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        btn_save = wx.Button(panel, label="Enregistrer")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        vbox.Add(btn_save, 0, wx.ALL | wx.CENTER, 5)
        btn_save.SetBackgroundColour(wx.Colour(0, 128, 0))
        btn_save.SetForegroundColour(wx.Colour(255, 255, 255))

        panel.SetSizer(vbox)

    def on_save(self, event):
        note_id = self.note[0]
        data = (
            self.etudiant_num_apogee_ctrl.GetValue(),
            self.module_id_ctrl.GetValue(),
            self.note_ctrl.GetValue()
        )
        if all(data):
            self.db.update_note(note_id, data)
            self.Close()
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)


class DeleteNoteDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Supprimer une Note", size=(400, 200))
        self.db = parent.db

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.etudiant_num_apogee_ctrl = wx.TextCtrl(panel)
        self.etudiant_num_apogee_ctrl.SetHint("Numéro Apogée Étudiant")
        vbox.Add(self.etudiant_num_apogee_ctrl, 0, wx.ALL | wx.EXPAND, 5)

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
        num_apogee = self.etudiant_num_apogee_ctrl.GetValue()
        module_id = self.module_id_ctrl.GetValue()

        if num_apogee and module_id:
            note = self.db.find_by_num_apogee_and_module(num_apogee, module_id)
            if note:
                self.db.delete_note(note[0])  # Deleting the note by its ID (note[0])
                self.EndModal(wx.ID_OK)
            else:
                wx.MessageBox("Aucune note trouvée pour ces critères", "Erreur", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Veuillez remplir tous les champs", "Erreur", wx.OK | wx.ICON_ERROR)



app = wx.App(False)
frame = MainFrame()
frame.Show()
app.MainLoop()
