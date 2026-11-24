# Device Metrics & Safe Zones

## Screen dimensions

Portrait. `pt` is the CSS/layout size; `px` is the physical raster you must deliver.

| Model | pt | px | Scale | Aspect |
| --- | --- | --- | --- | --- |
| iPhone 17 Pro Max / 16 Pro Max | 440×956 | 1320×2868 | @3x | 0.4603 |
| iPhone 17 Pro / 17 / 16 Pro | 402×874 | 1206×2622 | @3x | 0.4599 |
| iPhone Air | 420×912 | 1260×2736 | @3x | 0.4605 |
| iPhone 16 / 15 Pro / 14 Pro | 393×852 | 1179×2556 | @3x | 0.4613 |
| iPhone 16 Plus / 15 Pro Max / 15 Plus / 14 Pro Max | 430×932 | 1290×2796 | @3x | 0.4614 |
| **iPhone 16e / 14 / 13 / 13 Pro / 12 / 12 Pro** | **390×844** | **1170×2532** | @3x | 0.4621 |
| iPhone 14 Plus / 13 Pro Max / 12 Pro Max | 428×926 | 1284×2778 | @3x | 0.4622 |
| iPhone 13 mini / 12 mini / 11 Pro / X / XS | 375×812 | 1125×2436 | @3x | 0.4618 |
| iPhone 11 / XR | 414×896 | 828×1792 | @2x | 0.4621 |
| iPhone SE (4.7") / 8 / 7 | 375×667 | 750×1334 | @2x | 0.5622 |

**Render at the pt size with a device scale factor**, not at the px size with scale 1. Emulating
`390×844 @ deviceScaleFactor=3` gives you a genuine @3x raster with hinted text. Laying out at
1170 CSS px and downscaling gives you soft text and a layout at the wrong logical size.

## Lock screen occupancy (iOS 16+)

Fractions of total screen height. Approximate but reliable across recent models.

| Zone | Top | Bottom | Notes |
| --- | --- | --- | --- |
| Status bar (time, signal, battery) | 0% | ~6% | Always present |
| Notch / Dynamic Island | 0% | ~4% | Centred, ~33% of width |
| Date line | ~7% | ~9% | Always present |
| Clock | ~9% | ~27% | Very large; customisable font |
| Below-clock widget tray | ~27% | ~38% | Only if the user has widgets. Up to 4 small |
| **Free content band** | **~40%** | **~88%** | What your design actually gets |
| Notification stack | ~55% | ~88% | Transient, translucent, grows downward |
| Camera / flashlight buttons | ~88% | ~95% | Left and right edges only; centre stays clear |
| Home indicator | ~96% | ~99% | |

### Practical reservations

- **Widgets in use:** clear the top **40%**.
- **No widgets:** clear the top **30%**.
- **Bottom:** clear the last **8–10%**. Centred content may extend to ~92% because the
  camera/flashlight buttons hug the edges — but never below the home indicator.
- **Notifications** will cover anything from ~55% down. Put the single most important element
  as high in the free band as possible, and let secondary content take the overlap.

Always render a mock of the clock, date, and widget tray on top of the design before judging
its composition. A layout that looks balanced on a bare canvas reads as bottom-heavy once the
top 40% is full of system UI.

## Home screen widget canvases (WidgetKit)

For when a real widget is being built rather than a wallpaper. Sizes in pt for a 390×844 screen.

| Family | Size | Notes |
| --- | --- | --- |
| `systemSmall` | 158×158 | 2×2 grid cells |
| `systemMedium` | 338×158 | 4×2 |
| `systemLarge` | 338×354 | 4×4 |
| `systemExtraLarge` | iPad only | 8×4 |
| `accessoryCircular` | 76×76 | Lock screen, monochrome, vibrancy-tinted |
| `accessoryRectangular` | 172×76 | Lock screen, monochrome |
| `accessoryInline` | ~variable | Single line above the clock, monochrome |

Lock screen accessory widgets are rendered **monochrome with vibrancy** — colour is discarded.
Design them in tonal values only; anything that depends on hue will disappear.

## Corner radius

Screen corner radius is roughly **12% of width / 5.6% of height** for the modern rounded
models. Content within ~4% of any corner risks being clipped by the mask.
