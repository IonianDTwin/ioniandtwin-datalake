#!/usr/bin/env python3
"""Render a map for Data24 (Protected land %) - EL62 Ionian Islands.

Marks, on a map of the Ionian Islands (EL62, NUTS 2021, EPSG:3035 LAEA), the
portion of land under Natura 2000 protection (Habitats ∪ Birds ∩ EL62 land).
Two panels side by side:

  left  - "Protected land": the protected section marked in green over the islands.
  right - "Full Natura 2000 sites": the complete site polygons (mostly marine),
          to make the terrestrial/marine split visually obvious.

Also writes the derived protected-land geometry as GeoJSON (EPSG:4326) next to
the Data24 audit in data/curated/.

Outputs:
  data/samples/data24-protected-land-map-<date>.png
  data/curated/data24-protected-land.geojson
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from shapely.geometry import box
from shapely.ops import unary_union, transform
from shapely.validation import make_valid
import pyproj

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
SAMPLES = ROOT / "data" / "samples"
CURATED = ROOT / "data" / "curated"

EL62_PATH = RAW / "gisco-nuts-2021-3035-EL62.geojson"
HABITATS_PATH = RAW / "eea-natura2000-el62-envelope-habitats-4326.geojson"
BIRDS_PATH = RAW / "eea-natura2000-el62-envelope-birds-4326.geojson"
NUTS3_PATH = RAW / "gisco-nuts-2021-3035-LEVL_3.geojson"

CRS = "EPSG:3035"  # ETRS89 / LAEA Europe, equal-area, metres

# Short island labels for the four EL62 NUTS3 units.
NUTS3_LABELS = {
    "EL621": "Zakynthos",
    "EL622": "Kerkyra",
    "EL623": "Kefallinia & Ithaki",
    "EL624": "Lefkada",
}


def clean(geom):
    g = geom.buffer(0)
    if not g.is_valid:
        g = make_valid(g)
    return g


def load_el62() -> tuple:
    gdf = gpd.read_file(EL62_PATH).to_crs(CRS)
    return unary_union(gdf.geometry.tolist())


def load_natura() -> gpd.GeoDataFrame:
    hab = gpd.read_file(HABITATS_PATH).to_crs(CRS)
    birds = gpd.read_file(BIRDS_PATH).to_crs(CRS)
    return gpd.GeoDataFrame(
        {"kind": ["Habitats"] * len(hab) + ["Birds"] * len(birds)},
        geometry=list(hab.geometry) + list(birds.geometry),
        crs=CRS,
    )


def load_greek_context() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(NUTS3_PATH).to_crs(CRS)
    return gdf[gdf["NUTS_ID"].str.startswith("EL", na=False)].copy()


def add_scalebar(ax, x, y, km, label="50 km"):
    ax.plot([x, x + km * 1000], [y, y], color="#24292f", lw=1.6, solid_capstyle="butt")
    ax.plot([x, x], [y - 3000, y + 3000], color="#24292f", lw=1.2)
    ax.plot([x + km * 1000, x + km * 1000], [y - 3000, y + 3000], color="#24292f", lw=1.2)
    ax.text(x + km * 500, y + 4500, label, ha="center", va="bottom", fontsize=9, color="#24292f")


def add_north_arrow(ax, x, y):
    ax.add_patch(FancyArrowPatch((x, y), (x, y + 45000),
                 arrowstyle="-|>", mutation_scale=22, color="#24292f", lw=1.6))
    ax.text(x, y + 50000, "N", ha="center", va="bottom", fontsize=11, fontweight="bold", color="#24292f")


def plot_panel(ax, el62, natura, protected, context, title):
    # Context: western Greece + Peloponnese coastline for orientation.
    context.boundary.plot(ax=ax, color="#c8cdd3", linewidth=0.4)
    context.plot(ax=ax, color="#f0f2f5", edgecolor="none")

    # Full Natura 2000 sites (mostly marine) as a soft blue.
    gpd.GeoSeries([natura]).plot(ax=ax, color="#9ecae1", alpha=0.55, edgecolor="none")

    # EL62 islands on top.
    gpd.GeoSeries([el62]).plot(ax=ax, color="#fdfbf7", edgecolor="#57606a", linewidth=0.7)

    # Protected land marked in green.
    if protected is not None and not protected.is_empty:
        gpd.GeoSeries([protected]).plot(ax=ax, color="#2a9d5a", edgecolor="#1c6e3e", linewidth=0.4)

    ax.set_title(title, fontsize=11, fontweight="bold", pad=6)
    ax.set_axis_off()


def main() -> None:
    el62 = clean(load_el62())
    natura_gdf = load_natura()
    natura = clean(unary_union(natura_gdf.geometry.tolist()))
    protected = clean(natura.intersection(el62))

    context = load_greek_context()

    # Bounds around EL62 + margin (metres).
    minx, miny, maxx, maxy = el62.bounds
    mx = (maxx - minx) * 0.22 + 25000
    my = (maxy - miny) * 0.22 + 25000
    xlim = (minx - mx, maxx + mx)
    ylim = (miny - my, maxy + my)

    fig, axes = plt.subplots(1, 2, figsize=(16, 9), dpi=200)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.04, wspace=0.04)

    pct = protected.area / el62.area * 100
    km2 = protected.area / 1e6
    fig.suptitle(
        f"Data24 · Protected land - Ionian Islands (EL62)   |   {km2:.1f} km² protected = {pct:.2f} % of land area",
        fontsize=15, fontweight="bold", y=0.97,
    )

    plot_panel(axes[0], el62, natura, protected, context, "Protected land (Natura 2000 ∩ EL62)")
    plot_panel(axes[1], el62, natura, None, context, "Full Natura 2000 sites (incl. marine)")

    # Shared legend + island labels on the left panel.
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend = [
        Patch(facecolor="#2a9d5a", edgecolor="#1c6e3e", label="Protected land (Natura 2000 ∩ EL62)"),
        Patch(facecolor="#9ecae1", alpha=0.7, label="Natura 2000 sites (full extent)"),
        Patch(facecolor="#fdfbf7", edgecolor="#57606a", label="EL62 islands (land)"),
        Patch(facecolor="#f0f2f5", edgecolor="#c8cdd3", label="Mainland context"),
    ]
    axes[0].legend(handles=legend, loc="upper left", fontsize=8.5, frameon=True, framealpha=0.9)

    for ax in axes:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        # Island labels from the EL62 NUTS3 centroids.
        for _, row in context.iterrows():
            code = row["NUTS_ID"]
            if code in NUTS3_LABELS:
                c = row.geometry.centroid
                if c.within(box(*xlim, *ylim)):
                    ax.annotate(NUTS3_LABELS[code], (c.x, c.y), ha="center", va="center",
                                fontsize=8, fontstyle="italic", color="#33383d")

    # Scale bar + north arrow on the left panel (metres).
    sx = xlim[0] + 0.06 * (xlim[1] - xlim[0])
    sy = ylim[0] + 0.06 * (ylim[1] - ylim[0])
    add_scalebar(axes[0], sx, sy, 50)
    add_north_arrow(axes[1], xlim[1] - 0.09 * (xlim[1] - xlim[0]), ylim[0] + 0.06 * (ylim[1] - ylim[0]))

    # Data-source caption.
    fig.text(0.5, 0.01,
             "Sources: EEA Natura 2000 (ArcGIS REST) · Eurostat GISCO NUTS 2021 (EPSG:3035 LAEA). "
             "Protected = union(Habitats ∪ Birds) ∩ EL62 land. Echinades/Petalas islets are protected "
             "via a GR23-coded Acheloos-delta site (1,608 ha).",
             ha="center", fontsize=8, color="#57606a")

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    png = SAMPLES / f"data24-protected-land-map-{date}.png"
    png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # Derived protected-land geometry -> GeoJSON (EPSG:4326, GeoJSON convention).
    # Simplify at 10 m (EPSG:3035 metres) - far below the 1:1M GISCO boundary
    # accuracy - to keep the derived artifact lean; full-resolution raw stays in data/raw/.
    to4326 = pyproj.Transformer.from_crs(CRS, "EPSG:4326", always_xy=True).transform
    simplified = protected.simplify(10.0, preserve_topology=True)
    protected4326 = transform(to4326, simplified)
    gj = gpd.GeoDataFrame(geometry=[protected4326], crs="EPSG:4326")
    gj_path = CURATED / "data24-protected-land.geojson"
    gj.to_file(gj_path, driver="GeoJSON")

    print(f"map -> {png} ({png.stat().st_size} bytes)")
    print(f"geometry -> {gj_path}")
    print(f"protected land: {km2:.2f} km² = {pct:.2f} % of EL62 ({el62.area/1e6:.2f} km²)")


if __name__ == "__main__":
    main()
