import tkinter as tk
from tkinter import ttk
import os
from modules.indexing import load_documents, build_all_tfidf

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("TF-IDF Information Retrieval System")
        self.root.geometry("1000x700")
        self.root.state("zoomed")

        self.colors = {
            "bg_sidebar": "#1E293B",
            "bg_main": "#F8FAFC",
            "bg_card": "#FFFFFF",
            "text_primary": "#1E293B",
            "text_secondary": "#64748B",
            "accent_blue": "#2563EB",
            "accent_green": "#059669",
            "accent_hover": "#334155",
            "white": "#FFFFFF",
            "border": "#E2E8F0",
        }

        # Load documents & build TF-IDF
        self.documents = load_documents(DATA_PATH)
        (
            self.vocab,
            self.doc_ids,
            self.tf_raw,
            self.tf_normalized,
            self.df,
            self.idf,
            self.tfidf_matrix,
        ) = build_all_tfidf(self.documents)

        self.sidebar = tk.Frame(self.root, bg=self.colors["bg_sidebar"], width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_sidebar()
        self.show_home()

    def setup_sidebar(self):
        logo_frame = tk.Frame(self.sidebar, bg=self.colors["bg_sidebar"], pady=40)
        logo_frame.pack(fill=tk.X)

        tk.Label(
            logo_frame,
            text="TF-IDF",
            font=("Inter", 28, "bold"),
            fg=self.colors["white"],
            bg=self.colors["bg_sidebar"],
        ).pack()

        tk.Label(
            logo_frame,
            text="Information Retrieval System",
            font=("Inter", 10, "bold"),
            fg=self.colors["text_secondary"],
            bg=self.colors["bg_sidebar"],
        ).pack(pady=(5, 0))

        tk.Frame(self.sidebar, bg="#334155", height=1).pack(fill=tk.X, padx=20, pady=10)

        self.menu_items = []
        self.add_menu_item("🏠      Dashboard", self.show_home)
        self.add_menu_item("📂      Daftar Dokumen", self.open_documents)
        self.add_menu_item("📊      TF-IDF Matrix", self.open_tfidf_matrix)
        self.add_menu_item("🔍      Query & Ranking", self.open_query)

        footer = tk.Frame(self.sidebar, bg=self.colors["bg_sidebar"], pady=30)
        footer.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(
            footer,
            text="oleh",
            font=("Inter", 9),
            fg="#94A3B8",
            bg=self.colors["bg_sidebar"],
        ).pack()

        tk.Label(
            footer,
            text="Gede Yudhi Adinata",
            font=("Inter", 11, "bold"),
            fg=self.colors["white"],
            bg=self.colors["bg_sidebar"],
        ).pack()

        tk.Label(
            footer,
            text="2305551142",
            font=("Inter", 10),
            fg="#94A3B8",
            bg=self.colors["bg_sidebar"],
        ).pack()

    def add_menu_item(self, text, command):
        btn = tk.Button(
            self.sidebar,
            text=text,
            font=("Inter", 11),
            fg=self.colors["white"],
            bg=self.colors["bg_sidebar"],
            bd=0,
            padx=30,
            pady=15,
            anchor="w",
            cursor="hand2",
            activebackground=self.colors["accent_hover"],
            activeforeground=self.colors["white"],
            command=command,
        )
        btn.pack(fill=tk.X)
        self.menu_items.append(btn)

        btn.bind("<Enter>", lambda e: btn.config(bg=self.colors["accent_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.colors["bg_sidebar"]))

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main_area()

        from modules.interface import build_dashboard

        build_dashboard(
            self.main_area,
            self.colors,
            self.doc_ids,
            self.vocab,
            len(self.doc_ids),
            self.open_tfidf_matrix,
            self.open_query,
        )

    def inner_view_header(self, title):
        header = tk.Frame(
            self.main_area,
            bg=self.colors["white"],
            pady=20,
            padx=30,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text=title,
            font=("Inter", 18, "bold"),
            fg=self.colors["text_primary"],
            bg=self.colors["white"],
        ).pack(side=tk.LEFT)

    def open_tfidf_matrix(self):
        self.clear_main_area()
        self.inner_view_header("📊 TF-IDF Matrix & Perhitungan")

        inner_frame = tk.Frame(
            self.main_area, bg=self.colors["bg_main"], padx=20, pady=20
        )
        inner_frame.pack(fill=tk.BOTH, expand=True)

        from modules.interface import build_tfidf_matrix_view

        build_tfidf_matrix_view(
            inner_frame,
            self.colors,
            self.vocab,
            self.doc_ids,
            self.tf_raw,
            self.tf_normalized,
            self.df,
            self.idf,
            self.tfidf_matrix,
        )

    def open_documents(self):
        self.clear_main_area()
        self.inner_view_header("📂 Daftar Dokumen Sumber")

        from modules.interface import build_documents_view

        build_documents_view(self.main_area, self.colors, self.doc_ids, self.documents)

    def open_query(self):
        self.clear_main_area()
        self.inner_view_header("🔍 Query & Ranking TF-IDF")

        inner_frame = tk.Frame(
            self.main_area, bg=self.colors["bg_main"], padx=10, pady=10
        )
        inner_frame.pack(fill=tk.BOTH, expand=True)

        from modules.interface import build_query_view

        build_query_view(
            inner_frame,
            self.colors,
            self.vocab,
            self.doc_ids,
            self.idf,
            self.tfidf_matrix,
            self.documents,
        )


if __name__ == "__main__":
    root = tk.Tk()
    try:
        from tkinter import font

        font.nametofont("TkDefaultFont").configure(family="Inter", size=10)
    except:
        pass

    app = MainApplication(root)
    root.mainloop()
