# -*- mode: python -*-

block_cipher = None


a = Analysis(['stickify.py'],
             pathex=['C:\\Users\\ansonl\\development\\stickify-pusher'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [ ('logo.ico', 'C:\\Users\\ansonl\\development\\stickify-pusher\\logo.ico', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='stickify',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='logo.ico')