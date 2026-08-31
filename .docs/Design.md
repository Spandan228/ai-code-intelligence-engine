# 🎨 Reference Design Specification & Token Architecture (v2.0 Enterprise)

## 1. Color Palette Tokens & Semantic Mapping

```css
:root {
  /* Canvas & Surface Layers */
  --canvas-bg:           #f1f3f7;       /* Warm Alabaster canvas base */
  --card-surface:        #ffffff;       /* Pure white card surface */
  --sidebar-bg:          #f8fafc;       /* Soft off-white navigation rail */
  --surface-hover:       #f8fafc;       /* Table row / list item hover */
  --surface-subtle:      #f1f5f9;       /* Input backgrounds & subtle tags */

  /* Text & Content */
  --text-primary:        #111827;       /* Deep slate titles & key numbers */
  --text-secondary:      #475569;       /* Body copy & secondary descriptions */
  --text-muted:          #64748b;       /* Section overlines & captions */
  --text-dim:            #94a3b8;       /* Placeholders & disabled text */

  /* Semantic Brand & Accents */
  --brand-primary:       #f97316;       /* Warm Sunset Tangerine */
  --brand-primary-hover: #ea580c;       /* Deep Coral */
  --brand-tint:          #fff7ed;       /* 10% Tangerine wash for active pills */

  --status-success:      #10b981;       /* Fresh Mint Emerald */
  --status-success-tint: #ecfdf5;       /* Mint wash */
  --status-warning:      #f59e0b;       /* Honey Amber */
  --status-warning-tint: #fffbeb;       /* Amber wash */
  --status-error:        #ef4444;       /* Rose Red */
  --status-error-tint:   #fef2f2;       /* Rose wash */

  /* Borders & Dividers */
  --border-hairline:     rgba(0, 0, 0, 0.05);
  --border-subtle:       #e2e8f0;
  --border-default:      #cbd5e1;
}
```

---

## 2. Elevation & Ambient Shadows

```css
--shadow-ambient:   0px 1px 3px rgba(0, 0, 0, 0.02), 0px 8px 24px -4px rgba(0, 0, 0, 0.05);
--shadow-elevated:  0px 4px 6px -1px rgba(0, 0, 0, 0.03), 0px 14px 30px -4px rgba(0, 0, 0, 0.08);
--shadow-focus:     0 0 0 3px rgba(249, 115, 22, 0.25);
```

---

## 3. Typography Scale (Plus Jakarta Sans & JetBrains Mono)

- **Hero Metrics**: `28px`–`32px`, Bold (800), tight tracking (`-0.035em`), tabular lining numerals.
- **Card & Section Titles**: `16px`–`18px`, Semi-Bold (700), `-0.02em` tracking.
- **Sidebar & Navigation Labels**: `14px`, Medium (500), neutral slate.
- **Table Body & Body Text**: `13px`–`14px`, Regular (400) / Medium (500), `1.5` line height.
- **Section Overlines**: `11px`–`12px`, Bold (700), All-Caps, `+0.08em` tracking.
- **Code & Telemetry**: `JetBrains Mono`, `13px`, Regular / Semi-Bold.

---

## 4. Spacing & Radii Scale

- **Spatial Base**: Strict 8pt scale (`4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`, `48px`).
- **Corner Radii**:
  - `radius-sm`: `6px` (Badges, tags)
  - `radius-md`: `10px`–`12px` (Inputs, buttons, dropdowns)
  - `radius-lg`: `16px`–`20px` (Bento cards, panels)
  - `radius-pill`: `9999px` (Status pills, avatars)

---

## 5. Motion Foundation

```css
--ease-fluid:      cubic-bezier(0.16, 1, 0.3, 1);
--duration-fast:   180ms;
--duration-medium: 350ms;
```
