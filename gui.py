"""
Interface Pygame pour le Sudoku Solver.
Visualisation de la résolution par 5 algorithmes différents.
"""

import pygame
import sys
import copy
import time
import threading
import tracemalloc

from sudoku import SudokuGrid
from backtracking import resoudre_backtracking
from bruteforce import (
    resoudre_force_brute_iterative,
    resoudre_force_brute_exhaustive,
    bruteforce_aleatoire_memoire,
    bruteforce_exhaustif_aleatoire_memoire,
)

# ──────────────────────────────────────────────
# CONSTANTES
# ──────────────────────────────────────────────

WIDTH, HEIGHT = 600, 820
GRID_ORIGIN_X, GRID_ORIGIN_Y = 42, 100
CELL_SIZE = 56
GRID_SIZE = CELL_SIZE * 9  # 504

FPS = 30

# Couleurs
WHITE = (255, 255, 255)
BG_COLOR = (245, 245, 240)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BLUE = (41, 98, 255)
GREEN = (46, 125, 50)
RED = (211, 47, 47)
ACCENT = (41, 98, 255)
HOVER_COLOR = (232, 240, 254)
BTN_COLOR = (255, 255, 255)
BTN_BORDER = (180, 180, 180)
SOLVED_COLOR = (25, 118, 210)
INITIAL_COLOR = (33, 33, 33)
GRID_LINE = (33, 33, 33)
GRID_LINE_THIN = (189, 189, 189)
TITLE_BG = (41, 98, 255)
TITLE_BG_GREEN = (46, 125, 50)
STATS_BG = (250, 250, 250)
SELECTED_CELL_BG = (187, 222, 251)
ERROR_COLOR = (244, 67, 54)
ERROR_BG = (255, 235, 238)
SUCCESS_BG = (232, 245, 233)
PLAYER_COLOR = (46, 125, 50)

# Algorithmes
ALGORITHMS = [
    ("Backtracking", "backtracking"),
    ("Brute Force Aléatoire + Mémoire", "bruteforce_aleatoire_memoire"),
    ("Brute Force Itérative", "bruteforce_iterative"),
    ("Brute Force Exhaustive", "bruteforce_exhaustive"),
    ("Brute Force Exh. Aléatoire + Mémoire", "bruteforce_exhaustif_aleatoire_memoire"),
]

NB_GRILLES = 6
NB_GRILLES_JEU = 10


# ──────────────────────────────────────────────
# CLASSES UI
# ──────────────────────────────────────────────


class Button:
    """Bouton rectangulaire simple."""

    def __init__(self, x, y, w, h, text, font, color=BTN_COLOR, text_color=BLACK,
                 border_color=BTN_BORDER, hover=HOVER_COLOR, border_radius=8):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.border_color = border_color
        self.hover = hover
        self.border_radius = border_radius

    def draw(self, surface, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        bg = self.hover if is_hover else self.color

        # Ombre légère
        shadow_rect = self.rect.move(2, 2)
        pygame.draw.rect(surface, (220, 220, 220), shadow_rect, border_radius=self.border_radius)

        # Fond
        pygame.draw.rect(surface, bg, self.rect, border_radius=self.border_radius)
        # Bordure
        pygame.draw.rect(surface, self.border_color, self.rect, width=1, border_radius=self.border_radius)

        # Texte centré
        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ──────────────────────────────────────────────
# APPLICATION
# ──────────────────────────────────────────────


class SudokuApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()

        # Polices
        self.font_title = pygame.font.SysFont("Helvetica", 28, bold=True)
        self.font_btn = pygame.font.SysFont("Helvetica", 18)
        self.font_btn_sm = pygame.font.SysFont("Helvetica", 15)
        self.font_cell = pygame.font.SysFont("Helvetica", 26, bold=True)
        self.font_cell_solved = pygame.font.SysFont("Helvetica", 26)
        self.font_stats = pygame.font.SysFont("Helvetica", 14)
        self.font_subtitle = pygame.font.SysFont("Helvetica", 16)
        self.font_back = pygame.font.SysFont("Helvetica", 14, bold=True)

        # État
        self.state = "menu"  # menu | select_grid | view | select_grid_play | play
        self.selected_algo = None  # (label, key)
        self.selected_grid_num = None
        self.sudoku = None
        self.grille_originale = None
        self.grille_resolue = None
        self.solved = False
        self.solving = False
        self.stats = {}

        # État jeu libre
        self.play_grid = None        # grille en cours de jeu
        self.play_original = None    # grille originale (pour savoir quelles cases sont fixes)
        self.play_solution = None    # solution pour vérification
        self.play_selected = None    # (row, col) case sélectionnée
        self.play_errors = set()     # set de (row, col) avec erreurs
        self.play_won = False
        self.play_grid_num = None

        # Boutons — construits dynamiquement par chaque écran
        self.buttons = []

    # ──────────────────────────────────────────
    # BOUCLE PRINCIPALE
    # ──────────────────────────────────────────

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "view":
                            self.state = "select_grid"
                        elif self.state == "select_grid":
                            self.state = "menu"
                        elif self.state == "play":
                            self.state = "select_grid_play"
                        elif self.state == "select_grid_play":
                            self.state = "menu"
                        else:
                            running = False
                    elif self.state == "play":
                        self._handle_play_key(event)

            self.screen.fill(BG_COLOR)

            if self.state == "menu":
                self._draw_menu(mouse_pos)
            elif self.state == "select_grid":
                self._draw_select_grid(mouse_pos)
            elif self.state == "view":
                self._draw_view(mouse_pos)
            elif self.state == "select_grid_play":
                self._draw_select_grid_play(mouse_pos)
            elif self.state == "play":
                self._draw_play(mouse_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    # ──────────────────────────────────────────
    # GESTION DES CLICS
    # ──────────────────────────────────────────

    def _handle_click(self, pos):
        for btn, action in self.buttons:
            if btn.is_clicked(pos):
                action()
                return

        # Clic sur la grille en mode jeu libre
        if self.state == "play" and not self.play_won:
            ox, oy = GRID_ORIGIN_X, GRID_ORIGIN_Y
            x, y = pos
            if ox <= x < ox + GRID_SIZE and oy <= y < oy + GRID_SIZE:
                col = (x - ox) // CELL_SIZE
                row = (y - oy) // CELL_SIZE
                if 0 <= row < 9 and 0 <= col < 9:
                    if self.play_original[row][col] == 0:
                        self.play_selected = (row, col)
                    else:
                        self.play_selected = None

    # ──────────────────────────────────────────
    # ÉCRAN : MENU PRINCIPAL
    # ──────────────────────────────────────────

    def _draw_menu(self, mouse_pos):
        self.buttons = []

        # Titre
        self._draw_title_bar("SUDOKU SOLVER")

        # Sous-titre
        sub = self.font_subtitle.render("Choisissez un algorithme de résolution", True, DARK_GRAY)
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 80))

        # Boutons algorithmes
        btn_w, btn_h = 440, 52
        start_y = 130
        spacing = 66

        for i, (label, key) in enumerate(ALGORITHMS):
            y = start_y + i * spacing
            x = WIDTH // 2 - btn_w // 2
            btn = Button(x, y, btn_w, btn_h, label, self.font_btn,
                         border_color=ACCENT, text_color=INITIAL_COLOR)

            def make_action(algo_label=label, algo_key=key):
                def action():
                    self.selected_algo = (algo_label, algo_key)
                    self.state = "select_grid"
                return action

            btn.draw(self.screen, mouse_pos)
            self.buttons.append((btn, make_action()))

        # Séparateur
        sep_y = start_y + len(ALGORITHMS) * spacing + 15
        pygame.draw.line(self.screen, GRAY, (80, sep_y), (WIDTH - 80, sep_y), 1)

        # Bouton Jeu Libre
        play_btn = Button(WIDTH // 2 - btn_w // 2, sep_y + 20, btn_w, 52,
                          "🎮  Jeu Libre", self.font_btn,
                          color=WHITE, text_color=GREEN, border_color=GREEN)
        play_btn.draw(self.screen, mouse_pos)
        self.buttons.append((play_btn, lambda: setattr(self, 'state', 'select_grid_play')))

        # Bouton quitter
        quit_btn = Button(WIDTH // 2 - 80, sep_y + 90,
                          160, 42, "Quitter", self.font_btn_sm,
                          color=(245, 245, 245), text_color=RED, border_color=RED)
        quit_btn.draw(self.screen, mouse_pos)
        self.buttons.append((quit_btn, lambda: (pygame.quit(), sys.exit())))

    # ──────────────────────────────────────────
    # ÉCRAN : SÉLECTION DE GRILLE
    # ──────────────────────────────────────────

    def _draw_select_grid(self, mouse_pos):
        self.buttons = []

        algo_label = self.selected_algo[0] if self.selected_algo else ""
        self._draw_title_bar(algo_label)

        sub = self.font_subtitle.render("Choisissez une grille", True, DARK_GRAY)
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 80))

        # Boutons grilles — disposition 2×3
        btn_size = 120
        cols = 3
        gap = 30
        total_w = cols * btn_size + (cols - 1) * gap
        start_x = WIDTH // 2 - total_w // 2
        start_y = 130

        for i in range(NB_GRILLES):
            col = i % cols
            row = i // cols
            x = start_x + col * (btn_size + gap)
            y = start_y + row * (btn_size + gap)

            btn = Button(x, y, btn_size, btn_size, f"Grille {i + 1}", self.font_btn,
                         border_color=ACCENT, text_color=INITIAL_COLOR)

            def make_action(num=i + 1):
                def action():
                    self._load_grid(num)
                return action

            btn.draw(self.screen, mouse_pos)
            self.buttons.append((btn, make_action()))

        # Bouton retour
        back_btn = Button(20, HEIGHT - 55, 110, 38, "← Retour", self.font_back,
                          color=(245, 245, 245), text_color=DARK_GRAY, border_color=GRAY)
        back_btn.draw(self.screen, mouse_pos)
        self.buttons.append((back_btn, lambda: setattr(self, 'state', 'menu')))

    # ──────────────────────────────────────────
    # ÉCRAN : VISUALISATION
    # ──────────────────────────────────────────

    def _draw_view(self, mouse_pos):
        self.buttons = []

        algo_label = self.selected_algo[0] if self.selected_algo else ""
        self._draw_title_bar(f"{algo_label}  —  Grille {self.selected_grid_num}")

        # Grille
        self._draw_grid()

        # Boutons en bas
        y_btns = GRID_ORIGIN_Y + GRID_SIZE + 16

        # Bouton Résoudre
        if not self.solving and not self.solved:
            solve_btn = Button(WIDTH // 2 - 90, y_btns, 180, 42, "Résoudre", self.font_btn,
                               color=ACCENT, text_color=WHITE, border_color=ACCENT)
            solve_btn.draw(self.screen, mouse_pos)
            self.buttons.append((solve_btn, self._start_solve))

        # Message en cours
        if self.solving:
            txt = self.font_subtitle.render("Résolution en cours...", True, ACCENT)
            self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y_btns + 10))

        # Stats après résolution
        if self.solved and self.stats:
            self._draw_stats(y_btns)

        # Boutons navigation — placés tout en bas
        nav_y = HEIGHT - 60
        back_btn = Button(20, nav_y, 110, 38, "← Retour", self.font_back,
                          color=(245, 245, 245), text_color=DARK_GRAY, border_color=GRAY)
        back_btn.draw(self.screen, mouse_pos)

        def go_back():
            self.solved = False
            self.solving = False
            self.grille_resolue = None
            self.stats = {}
            self.state = "select_grid"

        self.buttons.append((back_btn, go_back))

        # Bouton reset (recharger la grille)
        if self.solved:
            reset_btn = Button(WIDTH - 150, nav_y, 130, 38, "Réinitialiser", self.font_back,
                               color=(245, 245, 245), text_color=ACCENT, border_color=ACCENT)
            reset_btn.draw(self.screen, mouse_pos)
            self.buttons.append((reset_btn, lambda: self._load_grid(self.selected_grid_num)))

    # ──────────────────────────────────────────
    # DESSIN DE LA GRILLE SUDOKU
    # ──────────────────────────────────────────

    def _draw_grid(self):
        grille_affichee = self.grille_resolue if self.grille_resolue else self.grille_originale
        if grille_affichee is None:
            return

        ox, oy = GRID_ORIGIN_X, GRID_ORIGIN_Y

        # Fond blanc pour la grille
        pygame.draw.rect(self.screen, WHITE,
                         (ox - 1, oy - 1, GRID_SIZE + 2, GRID_SIZE + 2))

        # Chiffres
        for i in range(9):
            for j in range(9):
                val = grille_affichee[i][j]
                x = ox + j * CELL_SIZE
                y = oy + i * CELL_SIZE

                if val != 0:
                    is_original = (self.grille_originale[i][j] != 0)
                    if is_original:
                        color = INITIAL_COLOR
                        font = self.font_cell
                    else:
                        color = SOLVED_COLOR
                        font = self.font_cell_solved
                        # Fond léger pour les cases résolues
                        pygame.draw.rect(self.screen, (232, 245, 253),
                                         (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

                    txt = font.render(str(val), True, color)
                    txt_rect = txt.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(txt, txt_rect)

        # Lignes fines
        for i in range(10):
            if i % 3 != 0:
                # Horizontale
                pygame.draw.line(self.screen, GRID_LINE_THIN,
                                 (ox, oy + i * CELL_SIZE),
                                 (ox + GRID_SIZE, oy + i * CELL_SIZE), 1)
                # Verticale
                pygame.draw.line(self.screen, GRID_LINE_THIN,
                                 (ox + i * CELL_SIZE, oy),
                                 (ox + i * CELL_SIZE, oy + GRID_SIZE), 1)

        # Lignes épaisses (blocs 3×3)
        for i in range(4):
            # Horizontale
            pygame.draw.line(self.screen, GRID_LINE,
                             (ox, oy + i * 3 * CELL_SIZE),
                             (ox + GRID_SIZE, oy + i * 3 * CELL_SIZE), 3)
            # Verticale
            pygame.draw.line(self.screen, GRID_LINE,
                             (ox + i * 3 * CELL_SIZE, oy),
                             (ox + i * 3 * CELL_SIZE, oy + GRID_SIZE), 3)

    # ──────────────────────────────────────────
    # STATS
    # ──────────────────────────────────────────

    def _draw_stats(self, y_start):
        stats = self.stats
        lines = []

        status = "✅ Résolu" if stats.get("solved") else "❌ Non résolu"
        lines.append(status)
        lines.append(f"Temps : {stats.get('time', 0):.4f}s")
        lines.append(f"Mémoire : {stats.get('mem_current', 0):.2f} Ko  (pic : {stats.get('mem_peak', 0):.2f} Ko)")

        if "operations" in stats:
            lines.append(f"Opérations : {stats['operations']:,}")
        if "tentatives" in stats:
            lines.append(f"Tentatives : {stats['tentatives']:,}")
        if "combinaisons_stockees" in stats:
            lines.append(f"Combinaisons stockées : {stats['combinaisons_stockees']:,}")
        if "combinaisons_testees" in stats:
            lines.append(f"Combinaisons testées : {stats['combinaisons_testees']:,}")
        if "total_possible" in stats:
            lines.append(f"Total possible : {stats['total_possible']:.2e}")

        # Dessiner le bloc stats
        x_start = 42
        bg_rect = pygame.Rect(x_start - 10, y_start - 4, GRID_SIZE + 20, len(lines) * 22 + 12)
        pygame.draw.rect(self.screen, STATS_BG, bg_rect, border_radius=6)
        pygame.draw.rect(self.screen, GRAY, bg_rect, width=1, border_radius=6)

        for i, line in enumerate(lines):
            color = GREEN if "✅" in line else (RED if "❌" in line else DARK_GRAY)
            txt = self.font_stats.render(line, True, color)
            self.screen.blit(txt, (x_start, y_start + i * 22 + 2))

    # ──────────────────────────────────────────
    # BARRE DE TITRE
    # ──────────────────────────────────────────

    def _draw_title_bar(self, text):
        pygame.draw.rect(self.screen, TITLE_BG, (0, 0, WIDTH, 60))
        txt = self.font_title.render(text, True, WHITE)
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 16))

    # ──────────────────────────────────────────
    # ACTIONS
    # ──────────────────────────────────────────

    def _load_grid(self, num):
        self.selected_grid_num = num
        self.sudoku = SudokuGrid("grilles.txt", num)
        self.grille_originale = copy.deepcopy(self.sudoku.grille)
        self.grille_resolue = None
        self.solved = False
        self.solving = False
        self.stats = {}
        self.state = "view"

    def _start_solve(self):
        if self.solving:
            return
        self.solving = True
        self.solved = False
        self.stats = {}

        thread = threading.Thread(target=self._solve_thread, daemon=True)
        thread.start()

    def _solve_thread(self):
        algo_key = self.selected_algo[1]
        grille_travail = copy.deepcopy(self.grille_originale)
        solved = False
        stats = {}

        tracemalloc.start()
        debut = time.perf_counter()
        nb_operations = [0]
        stats_aleatoire = []

        try:
            if algo_key == "backtracking":
                solved = resoudre_backtracking(grille_travail, nb_operations)
                stats["operations"] = nb_operations[0]

            elif algo_key == "bruteforce_iterative":
                solved = resoudre_force_brute_iterative(grille_travail)

            elif algo_key == "bruteforce_aleatoire_memoire":
                solved, tentatives, nb_stockees = bruteforce_aleatoire_memoire(
                    grille_travail, stats=stats_aleatoire
                )
                stats["tentatives"] = tentatives
                stats["combinaisons_stockees"] = nb_stockees

            elif algo_key == "bruteforce_exhaustive":
                solved, combinaisons, total = resoudre_force_brute_exhaustive(grille_travail)
                stats["combinaisons_testees"] = combinaisons
                stats["total_possible"] = total

            elif algo_key == "bruteforce_exhaustif_aleatoire_memoire":
                solved, tentatives, nb_stockees = bruteforce_exhaustif_aleatoire_memoire(
                    grille_travail, stats=stats_aleatoire
                )
                stats["tentatives"] = tentatives
                stats["combinaisons_stockees"] = nb_stockees

        except Exception:
            pass

        fin = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        stats["time"] = fin - debut
        stats["mem_current"] = current / 1024
        stats["mem_peak"] = peak / 1024
        stats["solved"] = solved

        self.grille_resolue = grille_travail
        self.stats = stats
        self.solved = True
        self.solving = False

    # ──────────────────────────────────────────
    # JEU LIBRE — SÉLECTION DE GRILLE
    # ──────────────────────────────────────────

    def _draw_select_grid_play(self, mouse_pos):
        self.buttons = []

        self._draw_title_bar_colored("JEU LIBRE", TITLE_BG_GREEN)

        sub = self.font_subtitle.render("Choisissez une grille", True, DARK_GRAY)
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 80))

        # Boutons grilles — disposition en grille
        btn_w, btn_h = 96, 56
        cols = 5
        gap = 12
        total_w = cols * btn_w + (cols - 1) * gap
        start_x = WIDTH // 2 - total_w // 2
        start_y = 120

        for i in range(NB_GRILLES_JEU):
            col = i % cols
            row = i // cols
            x = start_x + col * (btn_w + gap)
            y = start_y + row * (btn_h + gap)

            btn = Button(x, y, btn_w, btn_h, f"Grille {i + 1}", self.font_btn,
                         border_color=GREEN, text_color=INITIAL_COLOR)

            def make_action(num=i + 1):
                def action():
                    self._load_play_grid(num)
                return action

            btn.draw(self.screen, mouse_pos)
            self.buttons.append((btn, make_action()))

        # Bouton retour
        back_btn = Button(20, HEIGHT - 60, 110, 38, "← Retour", self.font_back,
                          color=(245, 245, 245), text_color=DARK_GRAY, border_color=GRAY)
        back_btn.draw(self.screen, mouse_pos)
        self.buttons.append((back_btn, lambda: setattr(self, 'state', 'menu')))

    # ──────────────────────────────────────────
    # JEU LIBRE — ÉCRAN DE JEU
    # ──────────────────────────────────────────

    def _draw_play(self, mouse_pos):
        self.buttons = []

        self._draw_title_bar_colored(f"Jeu Libre  —  Grille {self.play_grid_num}", TITLE_BG_GREEN)

        # Grille interactive
        self._draw_play_grid()

        # Message victoire
        y_msg = GRID_ORIGIN_Y + GRID_SIZE + 16
        if self.play_won:
            txt = self.font_title.render("🎉 Félicitations !", True, GREEN)
            self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y_msg))
            sub = self.font_subtitle.render("Grille résolue avec succès !", True, DARK_GRAY)
            self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, y_msg + 38))
        else:
            # Instructions
            instructions = [
                "Cliquez sur une case vide, puis tapez un chiffre (1-9)",
                "Suppr/Retour pour effacer  •  Les erreurs s'affichent en rouge",
            ]
            for idx, line in enumerate(instructions):
                txt = self.font_stats.render(line, True, DARK_GRAY)
                self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y_msg + idx * 20))

        # Boutons navigation
        nav_y = HEIGHT - 60
        back_btn = Button(20, nav_y, 110, 38, "← Retour", self.font_back,
                          color=(245, 245, 245), text_color=DARK_GRAY, border_color=GRAY)
        back_btn.draw(self.screen, mouse_pos)

        def go_back_play():
            self.play_selected = None
            self.play_won = False
            self.state = "select_grid_play"

        self.buttons.append((back_btn, go_back_play))

        # Bouton réinitialiser
        reset_btn = Button(WIDTH - 150, nav_y, 130, 38, "Réinitialiser", self.font_back,
                           color=(245, 245, 245), text_color=GREEN, border_color=GREEN)
        reset_btn.draw(self.screen, mouse_pos)
        self.buttons.append((reset_btn, lambda: self._load_play_grid(self.play_grid_num)))

        # Bouton vérifier
        if not self.play_won:
            check_btn = Button(WIDTH // 2 - 65, nav_y, 130, 38, "Vérifier", self.font_back,
                               color=(245, 245, 245), text_color=ACCENT, border_color=ACCENT)
            check_btn.draw(self.screen, mouse_pos)
            self.buttons.append((check_btn, self._check_play_grid))

    # ──────────────────────────────────────────
    # JEU LIBRE — DESSIN DE LA GRILLE
    # ──────────────────────────────────────────

    def _draw_play_grid(self):
        if self.play_grid is None:
            return

        ox, oy = GRID_ORIGIN_X, GRID_ORIGIN_Y

        # Fond blanc
        pygame.draw.rect(self.screen, WHITE,
                         (ox - 1, oy - 1, GRID_SIZE + 2, GRID_SIZE + 2))

        for i in range(9):
            for j in range(9):
                val = self.play_grid[i][j]
                x = ox + j * CELL_SIZE
                y = oy + i * CELL_SIZE

                # Fond de la case sélectionnée
                if self.play_selected == (i, j):
                    pygame.draw.rect(self.screen, SELECTED_CELL_BG,
                                     (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

                # Fond erreur
                if (i, j) in self.play_errors:
                    pygame.draw.rect(self.screen, ERROR_BG,
                                     (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

                # Fond victoire
                if self.play_won and self.play_original[i][j] == 0 and val != 0:
                    pygame.draw.rect(self.screen, SUCCESS_BG,
                                     (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))

                if val != 0:
                    is_original = (self.play_original[i][j] != 0)
                    if is_original:
                        color = INITIAL_COLOR
                        font = self.font_cell
                    elif (i, j) in self.play_errors:
                        color = ERROR_COLOR
                        font = self.font_cell_solved
                    else:
                        color = PLAYER_COLOR
                        font = self.font_cell_solved

                    txt = font.render(str(val), True, color)
                    txt_rect = txt.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(txt, txt_rect)

        # Lignes fines
        for i in range(10):
            if i % 3 != 0:
                pygame.draw.line(self.screen, GRID_LINE_THIN,
                                 (ox, oy + i * CELL_SIZE),
                                 (ox + GRID_SIZE, oy + i * CELL_SIZE), 1)
                pygame.draw.line(self.screen, GRID_LINE_THIN,
                                 (ox + i * CELL_SIZE, oy),
                                 (ox + i * CELL_SIZE, oy + GRID_SIZE), 1)

        # Lignes épaisses
        for i in range(4):
            pygame.draw.line(self.screen, GRID_LINE,
                             (ox, oy + i * 3 * CELL_SIZE),
                             (ox + GRID_SIZE, oy + i * 3 * CELL_SIZE), 3)
            pygame.draw.line(self.screen, GRID_LINE,
                             (ox + i * 3 * CELL_SIZE, oy),
                             (ox + i * 3 * CELL_SIZE, oy + GRID_SIZE), 3)

    # ──────────────────────────────────────────
    # JEU LIBRE — LOGIQUE
    # ──────────────────────────────────────────

    def _load_play_grid(self, num):
        self.play_grid_num = num
        sudoku = SudokuGrid("grilles_jeu.txt", num)
        self.play_original = copy.deepcopy(sudoku.grille)
        self.play_grid = copy.deepcopy(sudoku.grille)

        # Calculer la solution avec backtracking
        solution = copy.deepcopy(sudoku.grille)
        resoudre_backtracking(solution)
        self.play_solution = solution

        self.play_selected = None
        self.play_errors = set()
        self.play_won = False
        self.state = "play"

    def _handle_play_key(self, event):
        if self.play_selected is None or self.play_won:
            return

        row, col = self.play_selected

        # Chiffres 1-9
        if event.key in range(pygame.K_1, pygame.K_9 + 1):
            num = event.key - pygame.K_0
            self.play_grid[row][col] = num
            # Retirer l'erreur si corrigée
            self.play_errors.discard((row, col))
            # Vérifier victoire
            self._check_win()

        elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
            num = event.key - pygame.K_KP1 + 1
            self.play_grid[row][col] = num
            self.play_errors.discard((row, col))
            self._check_win()

        # Effacer
        elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
            self.play_grid[row][col] = 0
            self.play_errors.discard((row, col))

        # Navigation flèches
        elif event.key == pygame.K_UP and row > 0:
            self._select_next_empty(row - 1, col, -1, 0)
        elif event.key == pygame.K_DOWN and row < 8:
            self._select_next_empty(row + 1, col, 1, 0)
        elif event.key == pygame.K_LEFT and col > 0:
            self._select_next_empty(row, col - 1, 0, -1)
        elif event.key == pygame.K_RIGHT and col < 8:
            self._select_next_empty(row, col + 1, 0, 1)

    def _select_next_empty(self, row, col, drow, dcol):
        """Sélectionne la case si elle est modifiable, sinon reste."""
        if 0 <= row < 9 and 0 <= col < 9:
            if self.play_original[row][col] == 0:
                self.play_selected = (row, col)
            else:
                self.play_selected = (row, col)  # on permet de voir la sélection même sur les fixes

    def _check_play_grid(self):
        """Vérifie les erreurs par rapport à la solution."""
        self.play_errors = set()
        for i in range(9):
            for j in range(9):
                if self.play_original[i][j] == 0 and self.play_grid[i][j] != 0:
                    if self.play_grid[i][j] != self.play_solution[i][j]:
                        self.play_errors.add((i, j))

    def _check_win(self):
        """Vérifie si la grille est complète et correcte."""
        for i in range(9):
            for j in range(9):
                if self.play_grid[i][j] == 0:
                    return
                if self.play_grid[i][j] != self.play_solution[i][j]:
                    return
        self.play_won = True
        self.play_selected = None

    def _draw_title_bar_colored(self, text, color):
        pygame.draw.rect(self.screen, color, (0, 0, WIDTH, 60))
        txt = self.font_title.render(text, True, WHITE)
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 16))


# ──────────────────────────────────────────────
# POINT D'ENTRÉE
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = SudokuApp()
    app.run()
