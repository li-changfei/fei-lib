# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['tank_battle.py'],
             pathex=['boom.py', 'bullet.py', 'coonDB.py', 'enemy.py', 'enumClass.py', 'game_functions.py', 'game_stats.py', 'register.py', 'settings.py', 'tank.py', 'tank_battle.py', 'tank_map.py', 'wall.py', 'wallBrick.py', 'C:\\SVN\\fei-lib\\trunk\\TankBattle'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='tank_battle',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
