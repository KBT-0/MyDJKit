# MyDJKit

Claude ile Rekordbox setleri hazırlama: müzik bulma (Apple Music/gamdl), BPM/ton uyumlu seçim ve sıralama,
güvenli Rekordbox yazımı, Hot Cue ve geçiş rehberi. Küçük başladı; zamanla bir skill/tool'a dönüşecek.

- `CLAUDE.md`: değişmez kurallar (uyum, güvenlik, kullanıcı tercihleri)
- `.claude/skills/dj-set/`: set kurma akışı
- `djasistan/`: `camelot` (ton/tempo kuralları), `engine` (seçim+sıra), `audit` (denetim), `rbread` (salt-okunur DB), `libpool` (kütüphane adayları)
- `hooks/gate.py`: Rekordbox açıkken ya da set denetimden geçmemişken DB yazımını engeller
- Test: `python3 tests/test_rules.py`

DB okuma `rbread` için pyrekordbox + sqlcipher3 gerekir (`.dj-tool-evaluation/rekordbox-mcp/.venv`).
