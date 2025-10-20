import pygame
import os
from Template.UIConfigs import *
class AssetProvider:
    ASSETS = {}
    
    @classmethod
    def carregar_assets(cls):
        """Carrega e escala todos os assets do jogo."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            # MAP TILES
            cls.ASSETS['grass_claro'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_dir, 'maps', 'map1', 'titleset', 'grass1.png')).convert_alpha(),
                (TAMANHO_QUADRADO, TAMANHO_QUADRADO)
            )
            cls.ASSETS['grass_escuro'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_dir, 'maps', 'map1', 'titleset', 'grass2.png')).convert_alpha(),
                (TAMANHO_QUADRADO, TAMANHO_QUADRADO)
            )

            cls.ASSETS['scoreboard'] = pygame.image.load(os.path.join(base_dir, 'maps', 'map1', 'object', 'map_scoreboard.png')).convert_alpha()
            

            # CAIPORA
            cls.ASSETS['caipora_attack'] = [
                pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'characters', 'defense', 'caipora', f'caipora_attack{i}.png')).convert_alpha(),
                    (TAMANHO_CAIPORA, TAMANHO_CAIPORA)
                )
                for i in range(1, 3)
            ]
            cls.ASSETS['caipora_projectile'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_dir, 'characters', 'defense', 'caipora', 'caipora_arrow.png')).convert_alpha(),
                (30, 30)
            )

            # BICHO PAPÃO
            bp_walk = [
                pygame.image.load(os.path.join(base_dir, 'characters', 'enemies', 'bicho-papao', f'bp_walk{i}.png')).convert_alpha()
                for i in range(1, 5)
            ]
            cls.ASSETS['bp_walk'] = [
                pygame.transform.scale(pygame.transform.flip(img, True, False), (TAMANHO_BP, TAMANHO_BP))
                for img in bp_walk
            ]

            # GUARANÁ (moeda) - carregar com o mesmo padrão dos outros assets
            cls.ASSETS['guarana_coin'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_dir, 'maps', 'map1', 'object', 'guarana_coin.png')).convert_alpha(),
                (40, 40)
            )

            # MENU PAUSA
            cls.ASSETS.update({
                # Fundo do menu pausa
                'menu_pausa': pygame.image.load(
                    os.path.join(base_dir, 'menu_pause', 'menu_pausa.png')
                ).convert_alpha(),

                # Botão MÚSICA
                'btn_musica': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_musica.png')).convert_alpha(),
                    (200, 60)  # Largura, altura
                ),
                'btn_musica_hover': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_musica_click.png')).convert_alpha(),
                    (200, 60)
                ),

                # Botão EFEITO SONORO
                'btn_efeito': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_efeitoSonoro.png')).convert_alpha(),
                    (200, 60)
                ),
                'btn_efeito_hover': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_efeitoSonoro_click.png')).convert_alpha(),
                    (200, 60)
                ),

                # Botão TUTORIAL
                'btn_tutorial': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_tutorial.png')).convert_alpha(),
                    (200, 60)
                ),
                'btn_tutorial_hover': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_tutorial_click.png')).convert_alpha(),
                    (200, 60)
                ),

                # Botão Sair da Partida
                'btn_sair': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_sair_partida.png')).convert_alpha(),
                    (200, 60)
                ),
                'btn_sair_hover': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'botao_sair_partida_click.png')).convert_alpha(),
                    (200, 60)
                ),

                # Icone Som Normal
                'icon_som': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'icone_som_normal.png')).convert_alpha(),
                    (40, 40)
                ),
                'icon_som_hover': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'icone_som_click.png')).convert_alpha(),
                    (40, 40)
                ),

                # Icone Som Mudo
                'icon_mute': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'icone_som_mute.png')).convert_alpha(),
                    (40, 40)
                ),

                # Barra de volume
                'barra_volume_mute': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_0.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_mute_houver': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_0_click.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_25': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_25.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_25_houver': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_25_click.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_50': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_50.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_50_houver': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_50_click.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_75': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_75.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_75_houver': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_75_click.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_100': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_100.png')).convert_alpha(),
                    (150, 20)
                ),
                'barra_volume_100_houver': pygame.transform.scale(
                    pygame.image.load(os.path.join(base_dir, 'menu_pause', 'barra_100_click.png')).convert_alpha(),
                    (150, 20)
                ),
                
                # MENU PRINCIPAL
                'menu_principal': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen.png')
                ).convert_alpha(),
                
                # Botões do Menu Principal
                'menu_btn_jogar': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen_button3.png')
                ).convert_alpha(),
                'menu_btn_jogar_hover': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen_button_click1.png')
                ).convert_alpha(),
                
                'menu_btn_loja': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen_button2.png')
                ).convert_alpha(),
                'menu_btn_loja_hover': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen_button_click2.png')
                ).convert_alpha(),
                
                'menu_btn_creditos': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen_button1.png')
                ).convert_alpha(),
                'menu_btn_creditos_hover': pygame.image.load(
                    os.path.join(base_dir, 'menu', 'menu_screen', 'main_screen_button_click3.png')
                ).convert_alpha(),
                })

            print("Assets carregados com sucesso.")

        except pygame.error as e:
            print(f"ERRO CRÍTICO ao carregar assets: {e}")
            pygame.quit()
            exit()
            
    @classmethod
    def get(cls, key):
        """Método helper para acessar um asset."""
        return cls.ASSETS.get(key)