import tkinter as tk
from tkinter import ttk
import re
from modules.retrieval import tfidf_query


def create_stat_card(parent, title, value, icon, colors):
    card = tk.Frame(
        parent,
        bg=colors["bg_card"],
        padx=25,
        pady=25,
        highlightbackground=colors["border"],
        highlightthickness=1,
    )
    card.pack(side=tk.LEFT, padx=(0, 20), expand=True, fill=tk.BOTH)

    tk.Label(card, text=icon, font=("Inter", 24), bg=colors["bg_card"]).pack(anchor="w")
    tk.Label(
        card,
        text=value,
        font=("Inter", 28, "bold"),
        fg=colors["text_primary"],
        bg=colors["bg_card"],
    ).pack(anchor="w", pady=(10, 0))
    tk.Label(
        card,
        text=title,
        font=("Inter", 11, "bold"),
        fg=colors["text_secondary"],
        bg=colors["bg_card"],
    ).pack(anchor="w")


def create_feature_card(parent, title, description, color, command, colors):
    card = tk.Frame(
        parent,
        bg=colors["bg_card"],
        padx=30,
        pady=30,
        highlightbackground=colors["border"],
        highlightthickness=1,
    )
    card.pack(fill=tk.X, pady=(0, 20))

    text_frame = tk.Frame(card, bg=colors["bg_card"])
    text_frame.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(
        text_frame,
        text=title,
        font=("Inter", 16, "bold"),
        fg=colors["text_primary"],
        bg=colors["bg_card"],
    ).pack(anchor="w")

    tk.Label(
        text_frame,
        text=description,
        font=("Inter", 11),
        fg=colors["text_secondary"],
        bg=colors["bg_card"],
        wraplength=500,
        justify=tk.LEFT,
    ).pack(anchor="w", pady=(5, 0))

    btn = tk.Button(
        card,
        text="Buka →",
        font=("Inter", 11, "bold"),
        fg=colors["white"],
        bg=color,
        activebackground=colors["accent_hover"],
        activeforeground=colors["white"],
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=command,
    )
    btn.pack(side=tk.RIGHT, padx=10)


def build_dashboard(
    main_area, colors, doc_ids, vocab, total_docs, cmd_tfidf_matrix, cmd_query
):
    canvas = tk.Canvas(main_area, bg=colors["bg_main"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_area, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=colors["bg_main"])

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    container = tk.Frame(scrollable_frame, bg=colors["bg_main"], padx=60, pady=50)
    container.pack(fill=tk.BOTH, expand=True)

    tk.Label(
        container,
        text="Selamat Datang!",
        font=("Inter", 32, "bold"),
        fg=colors["text_primary"],
        bg=colors["bg_main"],
    ).pack(anchor="w")

    tk.Label(
        container,
        text="Sistem TF-IDF Information Retrieval — Menghitung bobot kata dan meranking dokumen berdasarkan query.",
        font=("Inter", 13),
        fg=colors["text_secondary"],
        bg=colors["bg_main"],
    ).pack(anchor="w", pady=(5, 30))

    stats_frame = tk.Frame(container, bg=colors["bg_main"])
    stats_frame.pack(fill=tk.X, pady=(0, 40))

    create_stat_card(stats_frame, "Total Dokumen", f"{total_docs}", "📄", colors)
    create_stat_card(stats_frame, "Total Terms (Unik)", f"{len(vocab)}", "🔤", colors)

    tk.Label(
        container,
        text="Fitur Utama",
        font=("Inter", 18, "bold"),
        fg=colors["text_primary"],
        bg=colors["bg_main"],
    ).pack(anchor="w", pady=(0, 20))

    card_container = tk.Frame(container, bg=colors["bg_main"])
    card_container.pack(fill=tk.X)

    create_feature_card(
        card_container,
        "📊 TF-IDF Matrix",
        "Visualisasi matrix TF-IDF lengkap beserta tabel TF, DF, IDF. Lihat bobot setiap kata di setiap dokumen dan temukan kata yang paling penting.",
        colors["accent_blue"],
        cmd_tfidf_matrix,
        colors,
    )

    create_feature_card(
        card_container,
        "🔍 Query & Ranking",
        "Masukkan query untuk mencari dokumen yang paling relevan. Sistem akan menghitung skor TF-IDF dan meranking dokumen berdasarkan nilai tertinggi.",
        colors["accent_green"],
        cmd_query,
        colors,
    )


def build_documents_view(main_area, colors, doc_ids, documents):
    container = tk.Frame(main_area, bg=colors["bg_main"], padx=30, pady=20)
    container.pack(fill=tk.BOTH, expand=True)

    list_frame = tk.Frame(
        container,
        bg=colors["white"],
        padx=15,
        pady=15,
        highlightbackground=colors["border"],
        highlightthickness=1,
    )
    list_frame.pack(side=tk.LEFT, fill=tk.Y)
    list_frame.config(width=300)
    list_frame.pack_propagate(False)

    tk.Label(
        list_frame,
        text="📑 Pilih Dokumen:",
        font=("Inter", 12, "bold"),
        bg=colors["white"],
        fg=colors["text_primary"],
    ).pack(anchor="w", pady=(0, 15))

    list_scroll = tk.Scrollbar(list_frame)
    list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(
        list_frame,
        font=("Inter", 11),
        bd=0,
        highlightthickness=0,
        selectbackground=colors["accent_blue"],
        selectforeground=colors["white"],
        activestyle="none",
        yscrollcommand=list_scroll.set,
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    list_scroll.config(command=listbox.yview)

    for doc_name in doc_ids:
        listbox.insert(tk.END, f" 📄 {doc_name}")

    content_frame = tk.Frame(
        container,
        bg=colors["white"],
        padx=30,
        pady=30,
        highlightbackground=colors["border"],
        highlightthickness=1,
    )
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

    header_frame = tk.Frame(content_frame, bg=colors["white"])
    header_frame.pack(fill=tk.X, pady=(0, 20))

    doc_title_lbl = tk.Label(
        header_frame,
        text="Isi Dokumen",
        font=("Inter", 16, "bold"),
        bg=colors["white"],
        fg=colors["text_primary"],
    )
    doc_title_lbl.pack(side=tk.LEFT)

    doc_meta_lbl = tk.Label(
        header_frame,
        text="0 Kata",
        font=("Inter", 11, "bold"),
        bg=colors["bg_main"],
        fg=colors["text_secondary"],
        padx=12,
        pady=5,
    )
    doc_meta_lbl.pack(side=tk.RIGHT)

    text_scroll = tk.Scrollbar(content_frame)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    doc_text_area = tk.Text(
        content_frame,
        font=("Consolas", 12),
        bd=0,
        padx=20,
        pady=20,
        bg="#F8FAFC",
        fg=colors["text_primary"],
        wrap=tk.WORD,
        state=tk.DISABLED,
        yscrollcommand=text_scroll.set,
        spacing1=5,
        spacing2=5,
        spacing3=5,
    )
    doc_text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_scroll.config(command=doc_text_area.yview)

    def on_select(evt):
        if not listbox.curselection():
            return
        index = int(listbox.curselection()[0])
        doc_name = doc_ids[index]

        content = documents[doc_name]
        word_count = len(content.split())

        doc_title_lbl.config(text=f"Isi: {doc_name}")
        doc_meta_lbl.config(text=f" {word_count} Kata ")

        doc_text_area.config(state=tk.NORMAL)
        doc_text_area.delete("1.0", tk.END)
        doc_text_area.insert(tk.END, content)
        doc_text_area.config(state=tk.DISABLED)

    listbox.bind("<<ListboxSelect>>", on_select)

    if doc_ids:
        listbox.selection_set(0)
        on_select(None)


def build_tfidf_matrix_view(
    parent, colors, vocab, doc_ids, tf_raw, tf_normalized, df, idf, tfidf_matrix
):
    """Membangun tampilan TF-IDF Matrix dengan beberapa tab: TF, DF/IDF, TF-IDF Matrix, Top Terms."""
    notebook = ttk.Notebook(parent)
    notebook.pack(fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Consolas", 10), rowheight=30, borderwidth=0)
    style.configure(
        "Treeview.Heading",
        font=("Inter", 10, "bold"),
        background=colors["bg_sidebar"],
        foreground="white",
        padding=4,
    )
    style.map("Treeview", background=[("selected", colors["accent_blue"])])

    tab_tfidf = tk.Frame(notebook, bg=colors["white"])
    notebook.add(tab_tfidf, text="TF-IDF Matrix")

    info_tfidf = tk.Frame(tab_tfidf, bg="#E8F4FD", pady=8, padx=15)
    info_tfidf.pack(fill=tk.X)
    tk.Label(
        info_tfidf,
        text="Matrix TF-IDF: TF-IDF(t,d) = TF(t,d) × IDF(t)  |  Nilai tinggi = kata penting dalam dokumen tersebut",
        font=("Inter", 10, "bold"),
        bg="#E8F4FD",
        fg="#1565C0",
    ).pack(anchor="w")

    table_frame_tfidf = tk.Frame(tab_tfidf, bg=colors["white"], padx=10, pady=10)
    table_frame_tfidf.pack(fill=tk.BOTH, expand=True)

    scrollbar_y_tfidf = tk.Scrollbar(table_frame_tfidf, orient=tk.VERTICAL)
    scrollbar_y_tfidf.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x_tfidf = tk.Scrollbar(table_frame_tfidf, orient=tk.HORIZONTAL)
    scrollbar_x_tfidf.pack(side=tk.BOTTOM, fill=tk.X)

    doc_labels = [d.replace(".txt", "") for d in doc_ids]
    columns_tfidf = ["term"] + doc_labels

    tree_tfidf = ttk.Treeview(
        table_frame_tfidf,
        columns=columns_tfidf,
        show="headings",
        yscrollcommand=scrollbar_y_tfidf.set,
        xscrollcommand=scrollbar_x_tfidf.set,
    )
    scrollbar_y_tfidf.config(command=tree_tfidf.yview)
    scrollbar_x_tfidf.config(command=tree_tfidf.xview)

    tree_tfidf.heading("term", text="Term", anchor="center")
    tree_tfidf.column("term", width=140, anchor="center")

    for doc_label in doc_labels:
        tree_tfidf.heading(doc_label, text=f"TF-IDF({doc_label})", anchor="center")
        tree_tfidf.column(doc_label, width=90, anchor="center")

    tree_tfidf.tag_configure("even", background="#FFFFFF")
    tree_tfidf.tag_configure("odd", background="#F8FAFC")
    tree_tfidf.tag_configure("highlight", background="#FFF3E0")

    for i, term in enumerate(vocab):
        values = [term]
        has_value = False
        for j in range(len(doc_ids)):
            val = tfidf_matrix[i][j]
            if val > 0:
                values.append(f"{val:.4f}")
                has_value = True
            else:
                values.append("0")
        tag = "even" if i % 2 == 0 else "odd"
        tree_tfidf.insert("", tk.END, values=values, tags=(tag,))

    tree_tfidf.pack(fill=tk.BOTH, expand=True)

    footer_tfidf = tk.Frame(tab_tfidf, bg="#E8F5E9", pady=6, padx=15)
    footer_tfidf.pack(fill=tk.X)
    tk.Label(
        footer_tfidf,
        text=f"Total terms: {len(vocab)}  |  Total dokumen: {len(doc_ids)}  |  "
        f"Nilai semakin tinggi menunjukkan kata semakin penting dalam dokumen tersebut",
        font=("Inter", 9, "bold"),
        bg="#E8F5E9",
        fg="#2E7D32",
    ).pack(anchor="w")

    tab_tf = tk.Frame(notebook, bg=colors["white"])
    notebook.add(tab_tf, text="Term Frequency (TF)")

    info_tf = tk.Frame(tab_tf, bg="#FFF3E0", pady=8, padx=15)
    info_tf.pack(fill=tk.X)
    tk.Label(
        info_tf,
        text="Term Frequency: TF(t,d) = jumlah kemunculan term t / total term dalam dokumen d",
        font=("Inter", 10, "bold"),
        bg="#FFF3E0",
        fg="#E65100",
    ).pack(anchor="w")

    table_frame_tf = tk.Frame(tab_tf, bg=colors["white"], padx=10, pady=10)
    table_frame_tf.pack(fill=tk.BOTH, expand=True)

    scrollbar_y_tf = tk.Scrollbar(table_frame_tf, orient=tk.VERTICAL)
    scrollbar_y_tf.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x_tf = tk.Scrollbar(table_frame_tf, orient=tk.HORIZONTAL)
    scrollbar_x_tf.pack(side=tk.BOTTOM, fill=tk.X)

    # Columns: Term | Raw(D1) | TF(D1) | Raw(D2) | TF(D2) | ...
    columns_tf = ["term"]
    for dl in doc_labels:
        columns_tf.append(f"raw_{dl}")
        columns_tf.append(f"tf_{dl}")

    tree_tf = ttk.Treeview(
        table_frame_tf,
        columns=columns_tf,
        show="headings",
        yscrollcommand=scrollbar_y_tf.set,
        xscrollcommand=scrollbar_x_tf.set,
    )
    scrollbar_y_tf.config(command=tree_tf.yview)
    scrollbar_x_tf.config(command=tree_tf.xview)

    tree_tf.heading("term", text="Term", anchor="center")
    tree_tf.column("term", width=140, anchor="center")

    for dl in doc_labels:
        tree_tf.heading(f"raw_{dl}", text=f"Count({dl})", anchor="center")
        tree_tf.column(f"raw_{dl}", width=75, anchor="center")
        tree_tf.heading(f"tf_{dl}", text=f"TF({dl})", anchor="center")
        tree_tf.column(f"tf_{dl}", width=85, anchor="center")

    tree_tf.tag_configure("even", background="#FFFFFF")
    tree_tf.tag_configure("odd", background="#F8FAFC")

    for i, term in enumerate(vocab):
        values = [term]
        for doc_id in doc_ids:
            raw_count = tf_raw[doc_id].get(term, 0)
            tf_val = tf_normalized[doc_id].get(term, 0)
            values.append(str(raw_count))
            values.append(f"{tf_val:.4f}" if tf_val > 0 else "0")
        tag = "even" if i % 2 == 0 else "odd"
        tree_tf.insert("", tk.END, values=values, tags=(tag,))

    tree_tf.pack(fill=tk.BOTH, expand=True)

    tab_dfidf = tk.Frame(notebook, bg=colors["white"])
    notebook.add(tab_dfidf, text="DF & IDF")

    info_dfidf = tk.Frame(tab_dfidf, bg="#F3E5F5", pady=8, padx=15)
    info_dfidf.pack(fill=tk.X)
    tk.Label(
        info_dfidf,
        text=f"DF = jumlah dokumen yang mengandung term  |  IDF = log₁₀(N/DF), N={len(doc_ids)}  |  IDF tinggi = kata jarang/unik",
        font=("Inter", 10, "bold"),
        bg="#F3E5F5",
        fg="#6A1B9A",
    ).pack(anchor="w")

    table_frame_dfidf = tk.Frame(tab_dfidf, bg=colors["white"], padx=10, pady=10)
    table_frame_dfidf.pack(fill=tk.BOTH, expand=True)

    scrollbar_y_dfidf = tk.Scrollbar(table_frame_dfidf, orient=tk.VERTICAL)
    scrollbar_y_dfidf.pack(side=tk.RIGHT, fill=tk.Y)

    tree_dfidf = ttk.Treeview(
        table_frame_dfidf,
        columns=("term", "df", "idf"),
        show="headings",
        yscrollcommand=scrollbar_y_dfidf.set,
    )
    scrollbar_y_dfidf.config(command=tree_dfidf.yview)

    tree_dfidf.heading("term", text="Term", anchor="center")
    tree_dfidf.heading("df", text="DF (Document Frequency)", anchor="center")
    tree_dfidf.heading("idf", text="IDF (Inverse Document Frequency)", anchor="center")
    tree_dfidf.column("term", width=200, anchor="center")
    tree_dfidf.column("df", width=250, anchor="center")
    tree_dfidf.column("idf", width=300, anchor="center")

    tree_dfidf.tag_configure("even", background="#FFFFFF")
    tree_dfidf.tag_configure("odd", background="#F8FAFC")
    tree_dfidf.tag_configure("high_idf", background="#E8F5E9")

    sorted_terms = sorted(vocab, key=lambda t: idf.get(t, 0), reverse=True)

    for i, term in enumerate(sorted_terms):
        df_val = df.get(term, 0)
        idf_val = idf.get(term, 0)
        idf_str = f"{idf_val:.6f}"
        tag = "even" if i % 2 == 0 else "odd"
        if idf_val >= 1.0:
            tag = "high_idf"
        tree_dfidf.insert("", tk.END, values=(term, df_val, idf_str), tags=(tag,))

    tree_dfidf.pack(fill=tk.BOTH, expand=True)

    tab_top = tk.Frame(notebook, bg=colors["white"])
    notebook.add(tab_top, text="Top Terms per Dokumen")

    info_top = tk.Frame(tab_top, bg="#E0F7FA", pady=8, padx=15)
    info_top.pack(fill=tk.X)
    tk.Label(
        info_top,
        text="Kata-kata paling penting (TF-IDF tertinggi) di setiap dokumen — menunjukkan topik utama dokumen",
        font=("Inter", 10, "bold"),
        bg="#E0F7FA",
        fg="#006064",
    ).pack(anchor="w")

    top_canvas = tk.Canvas(tab_top, bg=colors["white"], highlightthickness=0)
    top_scrollbar = ttk.Scrollbar(tab_top, orient="vertical", command=top_canvas.yview)
    top_scrollable = tk.Frame(top_canvas, bg=colors["white"])

    top_scrollable.bind(
        "<Configure>",
        lambda e: top_canvas.configure(scrollregion=top_canvas.bbox("all")),
    )

    top_window_id = top_canvas.create_window((0, 0), window=top_scrollable, anchor="nw")
    top_canvas.bind(
        "<Configure>", lambda e: top_canvas.itemconfig(top_window_id, width=e.width)
    )
    top_canvas.configure(yscrollcommand=top_scrollbar.set)

    top_canvas.pack(side="left", fill="both", expand=True)
    top_scrollbar.pack(side="right", fill="y")

    # Build top terms for each document
    top_n = 5
    for j, doc_id in enumerate(doc_ids):
        doc_label = doc_id.replace(".txt", "")

        card = tk.Frame(
            top_scrollable,
            bg=colors["bg_card"],
            padx=20,
            pady=15,
            highlightbackground=colors["border"],
            highlightthickness=1,
        )
        card.pack(fill=tk.X, padx=20, pady=(10, 5))

        tk.Label(
            card,
            text=f"📄 {doc_label}",
            font=("Inter", 13, "bold"),
            fg=colors["text_primary"],
            bg=colors["bg_card"],
        ).pack(anchor="w")

        # Get top terms for this document
        term_scores = []
        for i, term in enumerate(vocab):
            val = tfidf_matrix[i][j]
            if val > 0:
                term_scores.append((term, val))

        term_scores.sort(key=lambda x: x[1], reverse=True)
        top_terms = term_scores[:top_n]

        if top_terms:
            terms_text = "  |  ".join([f"{t}: {v:.4f}" for t, v in top_terms])
            tk.Label(
                card,
                text=f"Top {min(top_n, len(top_terms))} kata penting: {terms_text}",
                font=("Consolas", 10),
                fg="#1565C0",
                bg=colors["bg_card"],
                wraplength=900,
                justify=tk.LEFT,
            ).pack(anchor="w", pady=(5, 0))
        else:
            tk.Label(
                card,
                text="Tidak ada term dengan TF-IDF > 0",
                font=("Consolas", 10),
                fg="#999999",
                bg=colors["bg_card"],
            ).pack(anchor="w", pady=(5, 0))


def build_query_view(parent, colors, vocab, doc_ids, idf, tfidf_matrix, documents):
    """Tampilan pencarian query dengan TF-IDF ranking."""

    header = tk.Frame(parent, bg="#1A237E", pady=12, padx=20)
    header.pack(fill=tk.X)
    tk.Label(
        header,
        text="🔍 PENCARIAN QUERY TF-IDF",
        font=("Inter", 14, "bold"),
        fg="white",
        bg="#1A237E",
    ).pack(anchor="w")
    tk.Label(
        header,
        text="Masukkan kata kunci untuk mencari dokumen paling relevan berdasarkan skor TF-IDF",
        font=("Inter", 10),
        fg="#B3B9D1",
        bg="#1A237E",
    ).pack(anchor="w")

    input_frame = tk.Frame(parent, padx=20, pady=15, bg=colors["bg_main"])
    input_frame.pack(fill=tk.X)

    tk.Label(
        input_frame,
        text="Masukkan Query:",
        font=("Inter", 12, "bold"),
        bg=colors["bg_main"],
        fg=colors["text_primary"],
    ).pack(anchor="w")

    tk.Label(
        input_frame,
        text='Contoh: "Kucing Persia", "Kaki Pendek", "Raksasa Lembut", "Ekor Pendek", "Hidung Pesek"',
        font=("Inter", 9),
        fg="#888888",
        bg=colors["bg_main"],
    ).pack(anchor="w", pady=(0, 8))

    entry_frame = tk.Frame(input_frame, bg=colors["bg_main"])
    entry_frame.pack(fill=tk.X)

    query_entry = tk.Entry(entry_frame, font=("Consolas", 14), width=50)
    query_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=6)

    result_container = tk.Frame(parent, bg=colors["bg_main"], padx=20, pady=5)
    result_container.pack(fill=tk.BOTH, expand=True)

    result_info = tk.Label(
        result_container,
        text="",
        font=("Inter", 12, "bold"),
        fg=colors["text_primary"],
        bg=colors["bg_main"],
    )
    result_info.pack(anchor="w", pady=(0, 5))

    # Notebook for results
    result_notebook = ttk.Notebook(result_container)

    # Tab 1: Detail Perhitungan
    tab_detail = tk.Frame(result_notebook, bg=colors["white"])

    detail_scroll = tk.Scrollbar(tab_detail, orient=tk.VERTICAL)
    detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    detail_text = tk.Text(
        tab_detail,
        wrap=tk.WORD,
        font=("Consolas", 11),
        yscrollcommand=detail_scroll.set,
        state="disabled",
        bg="#F5F5F5",
        padx=15,
        pady=15,
    )
    detail_scroll.config(command=detail_text.yview)
    detail_text.pack(fill=tk.BOTH, expand=True)

    # Tab 2: Skor per Term
    tab_scores = tk.Frame(result_notebook, bg=colors["white"])

    # Tab 3: Dokumen Hasil
    tab_docs = tk.Frame(result_notebook, bg=colors["white"])

    doc_scroll = tk.Scrollbar(tab_docs, orient=tk.VERTICAL)
    doc_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    doc_result_text = tk.Text(
        tab_docs,
        wrap=tk.WORD,
        font=("Inter", 11),
        yscrollcommand=doc_scroll.set,
        state="disabled",
        bg="#FAFAFA",
        padx=15,
        pady=15,
    )
    doc_scroll.config(command=doc_result_text.yview)

    doc_result_text.tag_configure(
        "doc_id", font=("Inter", 13, "bold"), foreground="#1A237E"
    )
    doc_result_text.tag_configure(
        "score", font=("Consolas", 11, "bold"), foreground="#2E7D32"
    )
    doc_result_text.tag_configure(
        "highlight",
        font=("Inter", 11, "bold"),
        background="#FFFF00",
        foreground="black",
    )
    doc_result_text.tag_configure("separator", foreground="#CCCCCC")
    doc_result_text.tag_configure(
        "rank", font=("Inter", 12, "bold"), foreground="#D84315"
    )

    doc_result_text.pack(fill=tk.BOTH, expand=True)

    def execute_search(event=None):
        query = query_entry.get().strip()

        if not query:
            result_info.config(
                text="⚠️ Query kosong! Silakan masukkan kata kunci.", fg="red"
            )
            result_notebook.pack_forget()
            return

        query_terms, term_scores, doc_scores, ranked_docs, detail_str = tfidf_query(
            query, vocab, doc_ids, idf, tfidf_matrix
        )

        if not query_terms:
            result_info.config(
                text="⚠️ Query tidak menghasilkan token setelah preprocessing.", fg="red"
            )
            result_notebook.pack_forget()
            return

        result_notebook.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        for tab in result_notebook.tabs():
            result_notebook.forget(tab)

        tab_detail_new = tk.Frame(result_notebook, bg=colors["white"])
        result_notebook.add(tab_detail_new, text="📋 Detail Perhitungan")

        detail_scroll_new = tk.Scrollbar(tab_detail_new, orient=tk.VERTICAL)
        detail_scroll_new.pack(side=tk.RIGHT, fill=tk.Y)

        detail_text_new = tk.Text(
            tab_detail_new,
            wrap=tk.WORD,
            font=("Consolas", 11),
            yscrollcommand=detail_scroll_new.set,
            state="disabled",
            bg="#F5F5F5",
            padx=15,
            pady=15,
        )
        detail_scroll_new.config(command=detail_text_new.yview)
        detail_text_new.pack(fill=tk.BOTH, expand=True)

        detail_text_new.config(state="normal")
        detail_text_new.delete("1.0", tk.END)
        detail_text_new.insert(tk.END, detail_str)
        detail_text_new.config(state="disabled")

        tab_scores_new = tk.Frame(result_notebook, bg=colors["white"])
        result_notebook.add(tab_scores_new, text="📊 Skor TF-IDF per Term")

        scores_info = tk.Frame(tab_scores_new, bg="#E8F4FD", pady=6, padx=15)
        scores_info.pack(fill=tk.X)
        tk.Label(
            scores_info,
            text="Nilai TF-IDF setiap kata query di setiap dokumen (nilai 0 berarti kata tidak ada di dokumen tersebut)",
            font=("Inter", 9, "bold"),
            bg="#E8F4FD",
            fg="#1565C0",
        ).pack(anchor="w")

        scores_table_frame = tk.Frame(
            tab_scores_new, bg=colors["white"], padx=10, pady=10
        )
        scores_table_frame.pack(fill=tk.BOTH, expand=True)

        scores_scroll_y = tk.Scrollbar(scores_table_frame, orient=tk.VERTICAL)
        scores_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scores_scroll_x = tk.Scrollbar(scores_table_frame, orient=tk.HORIZONTAL)
        scores_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        doc_labels_short = [d.replace(".txt", "") for d in doc_ids]
        score_columns = ["term", "idf"] + doc_labels_short + ["info"]

        tree_scores = ttk.Treeview(
            scores_table_frame,
            columns=score_columns,
            show="headings",
            yscrollcommand=scores_scroll_y.set,
            xscrollcommand=scores_scroll_x.set,
        )
        scores_scroll_y.config(command=tree_scores.yview)
        scores_scroll_x.config(command=tree_scores.xview)

        tree_scores.heading("term", text="Query Term", anchor="center")
        tree_scores.column("term", width=120, anchor="center")
        tree_scores.heading("idf", text="IDF", anchor="center")
        tree_scores.column("idf", width=90, anchor="center")

        for dl in doc_labels_short:
            tree_scores.heading(dl, text=f"TF-IDF({dl})", anchor="center")
            tree_scores.column(dl, width=90, anchor="center")

        tree_scores.heading("info", text="Dokumen Tertinggi", anchor="center")
        tree_scores.column("info", width=160, anchor="center")

        tree_scores.tag_configure("even", background="#FFFFFF")
        tree_scores.tag_configure("odd", background="#F8FAFC")

        for i, term in enumerate(query_terms):
            idf_val = idf.get(term, 0)
            values = [term, f"{idf_val:.4f}"]

            max_doc = ""
            max_val = 0
            for doc_id in doc_ids:
                val = term_scores[term].get(doc_id, 0.0)
                if val > 0:
                    values.append(f"{val:.4f}")
                else:
                    values.append("0")
                if val > max_val:
                    max_val = val
                    max_doc = doc_id.replace(".txt", "")

            if max_doc:
                values.append(f"{max_doc} ({max_val:.4f})")
            else:
                values.append("N/A")

            tag = "even" if i % 2 == 0 else "odd"
            tree_scores.insert("", tk.END, values=values, tags=(tag,))

        # Add total score row
        total_values = ["TOTAL SKOR", "-"]
        for doc_id in doc_ids:
            total = doc_scores.get(doc_id, 0.0)
            if total > 0:
                total_values.append(f"{total:.4f}")
            else:
                total_values.append("0")
        if ranked_docs:
            total_values.append(f"🏆 {ranked_docs[0][0].replace('.txt', '')}")
        else:
            total_values.append("-")

        tree_scores.tag_configure(
            "total_row", background="#E8F5E9", font=("Inter", 10, "bold")
        )
        tree_scores.insert("", tk.END, values=total_values, tags=("total_row",))

        tree_scores.pack(fill=tk.BOTH, expand=True)

        # ---- Tab Dokumen Hasil ----
        tab_docs_new = tk.Frame(result_notebook, bg=colors["white"])
        result_notebook.add(
            tab_docs_new, text=f"📄 Dokumen Relevan ({len(ranked_docs)})"
        )

        doc_scroll_new = tk.Scrollbar(tab_docs_new, orient=tk.VERTICAL)
        doc_scroll_new.pack(side=tk.RIGHT, fill=tk.Y)

        doc_result_new = tk.Text(
            tab_docs_new,
            wrap=tk.WORD,
            font=("Inter", 11),
            yscrollcommand=doc_scroll_new.set,
            state="disabled",
            bg="#FAFAFA",
            padx=15,
            pady=15,
        )
        doc_scroll_new.config(command=doc_result_new.yview)

        doc_result_new.tag_configure(
            "doc_id", font=("Inter", 13, "bold"), foreground="#1A237E"
        )
        doc_result_new.tag_configure(
            "score", font=("Consolas", 11, "bold"), foreground="#2E7D32"
        )
        doc_result_new.tag_configure(
            "highlight",
            font=("Inter", 11, "bold"),
            background="#FFFF00",
            foreground="black",
        )
        doc_result_new.tag_configure("separator", foreground="#CCCCCC")
        doc_result_new.tag_configure(
            "rank", font=("Inter", 12, "bold"), foreground="#D84315"
        )

        doc_result_new.config(state="normal")
        doc_result_new.delete("1.0", tk.END)

        if ranked_docs:
            result_info.config(
                text=f'✅ Ditemukan {len(ranked_docs)} dokumen relevan untuk "{query}" (token: {query_terms})',
                fg="#2E7D32",
            )

            escaped_keywords = [re.escape(k) for k in query.split() if len(k) > 0]
            pattern = (
                re.compile(f"({'|'.join(escaped_keywords)})", re.IGNORECASE)
                if escaped_keywords
                else None
            )

            for rank_num, (doc_id, score) in enumerate(ranked_docs, 1):
                content = documents[doc_id]

                doc_result_new.insert(
                    tk.END,
                    f"  #{rank_num}  ",
                    "rank",
                )
                doc_result_new.insert(
                    tk.END,
                    f"📄 {doc_id}",
                    "doc_id",
                )
                doc_result_new.insert(
                    tk.END,
                    f"   [Skor: {score:.6f}]\n",
                    "score",
                )

                term_detail_parts = []
                for term in query_terms:
                    val = term_scores[term].get(doc_id, 0.0)
                    if val > 0:
                        term_detail_parts.append(f'"{term}"={val:.4f}')
                if term_detail_parts:
                    doc_result_new.insert(
                        tk.END,
                        f"   Rincian: {' + '.join(term_detail_parts)}\n\n",
                        "score",
                    )

                start_index = doc_result_new.index(tk.INSERT)
                doc_result_new.insert(tk.END, f"{content}\n")

                if pattern:
                    for match in pattern.finditer(content):
                        start_pos = match.start()
                        end_pos = match.end()
                        idx_start = f"{start_index}+{start_pos}c"
                        idx_end = f"{start_index}+{end_pos}c"
                        doc_result_new.tag_add("highlight", idx_start, idx_end)

                doc_result_new.insert(tk.END, "\n" + "─" * 100 + "\n\n", "separator")
        else:
            result_info.config(
                text=f'❌ Tidak ada dokumen yang mengandung kata "{query}" (token: {query_terms})',
                fg="red",
            )
            doc_result_new.insert(tk.END, "Tidak ada dokumen yang relevan ditemukan.\n")

        doc_result_new.config(state="disabled")
        doc_result_new.pack(fill=tk.BOTH, expand=True)

    btn_search = tk.Button(
        entry_frame,
        text="🔍 Cari & Ranking",
        font=("Inter", 12, "bold"),
        bg="#1A237E",
        fg="white",
        padx=20,
        pady=5,
        cursor="hand2",
        command=execute_search,
    )
    btn_search.pack(side=tk.LEFT)

    query_entry.bind("<Return>", execute_search)
