"""Plotly chart functions — dark OSRS theme."""

from typing import Dict, List, Optional
import numpy as np
import plotly.graph_objects as go

try:
    from ..utils import (
        format_gp,
        get_clean_item_name,
        get_item_tier_color,
        get_tier_from_name,
        CATEGORY_COLORS,
        CHART_COLORS,
    )
except ImportError:
    from utils import (
        format_gp,
        get_clean_item_name,
        get_item_tier_color,
        get_tier_from_name,
        CATEGORY_COLORS,
        CHART_COLORS,
    )

# Dark theme constants
_BG_PLOT = 'rgba(27,27,27,0.9)'
_BG_PAPER = 'rgba(0,0,0,0)'
_GRID_COLOR = 'rgba(90,74,42,0.3)'
_TEXT_YELLOW = '#ffff00'
_TEXT_ORANGE = '#ff981f'
_TEXT_LIGHT = '#d4c5a0'
_TEXT_GRAY = '#aaaaaa'
_BORDER_GOLD = '#5a4a2a'


def _dark_layout(**overrides) -> dict:
    """Base dark layout for all charts."""
    base = dict(
        paper_bgcolor=_BG_PAPER,
        plot_bgcolor=_BG_PLOT,
        font=dict(color=_TEXT_LIGHT, size=11),
        margin=dict(l=55, r=20, t=60, b=50),
    )
    base.update(overrides)
    return base


def _dark_axis(title: str = "", **overrides) -> dict:
    """Standard dark axis config."""
    base = dict(
        title=title,
        title_font=dict(color=_TEXT_ORANGE, size=11),
        tickfont=dict(color=_TEXT_LIGHT, size=9),
        gridcolor=_GRID_COLOR,
    )
    base.update(overrides)
    return base


def _dark_legend(**overrides) -> dict:
    """Standard dark legend config."""
    base = dict(
        font=dict(color=_TEXT_LIGHT, size=10),
        bgcolor='rgba(43,43,43,0.9)',
        bordercolor=_BORDER_GOLD,
        borderwidth=1,
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
    )
    base.update(overrides)
    return base


def create_profit_chart(results: List[Dict], top_n: int = 10) -> go.Figure:
    """Horizontal bar chart of top profitable chains."""
    sorted_results = sorted(results, key=lambda x: x.get("_profit_raw", 0), reverse=True)[:top_n]

    items = [r["Item"] for r in sorted_results]
    profits = [r["_profit_raw"] for r in sorted_results]
    categories = [r.get("Category", "Unknown") for r in sorted_results]

    display_names = [get_clean_item_name(name) for name in items]
    tiers = [get_tier_from_name(name) for name in items]
    colors = [get_item_tier_color(items[i], profits[i]) for i in range(len(items))]

    fig = go.Figure(data=[
        go.Bar(
            x=profits,
            y=display_names,
            orientation='h',
            marker_color=colors,
            marker_line_color=_BORDER_GOLD,
            marker_line_width=1.5,
            text=[format_gp(p) for p in profits],
            textposition='outside',
            textfont=dict(color=_TEXT_YELLOW, size=10),
            name='Profit',
            customdata=list(zip(categories, tiers)),
            hovertemplate='<b>%{y}</b><br>Category: %{customdata[0]}<br>Tier: %{customdata[1]}<br>Profit: %{x:,.0f} GP<extra></extra>'
        )
    ])

    fig.update_layout(
        **_dark_layout(
            height=max(380, top_n * 36),
            margin=dict(l=140, r=80, t=60, b=45),
            showlegend=False,
        ),
        title=dict(
            text="Top Profitable Chains",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text=f"Top {len(sorted_results)} by profit",
                font=dict(color=_TEXT_GRAY, size=10)
            )
        ),
        xaxis=_dark_axis("Net Profit (GP)", tickformat=',.0f'),
        yaxis=_dark_axis("", autorange="reversed"),
    )

    return fig


def create_category_pie(results: List[Dict]) -> go.Figure:
    """Pie chart of profit distribution by category."""
    category_profits = {}
    category_counts = {}

    for r in results:
        cat = r.get("Category", "Unknown")
        profit = max(0, r.get("_profit_raw", 0))
        category_profits[cat] = category_profits.get(cat, 0) + profit
        category_counts[cat] = category_counts.get(cat, 0) + 1

    sorted_cats = sorted(category_profits.items(), key=lambda x: x[1], reverse=True)
    total_profit = sum(category_profits.values())

    main_cats = []
    other_total = 0
    other_count = 0
    threshold = total_profit * 0.02

    for cat, profit in sorted_cats:
        if profit >= threshold:
            main_cats.append((cat, profit, category_counts[cat]))
        else:
            other_total += profit
            other_count += category_counts.get(cat, 0)

    if other_total > 0:
        main_cats.append(("Other", other_total, other_count))

    labels = [c[0] for c in main_cats]
    values = [c[1] for c in main_cats]
    counts = [c[2] for c in main_cats]

    colors = [CATEGORY_COLORS.get(label, '#8e44ad') for label in labels]

    hover_text = [
        f"<b>{label}</b><br>"
        f"Total Profit: {format_gp(val)}<br>"
        f"Chains: {cnt}<br>"
        f"Share: {val/total_profit*100:.1f}%"
        for label, val, cnt in zip(labels, values, counts)
    ]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(color=_TEXT_LIGHT, size=10),
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(
                colors=colors,
                line=dict(color=_BORDER_GOLD, width=2)
            ),
            pull=[0.03 if i == 0 else 0 for i in range(len(labels))],
            insidetextorientation='horizontal',
            sort=False
        )
    ])

    fig.add_annotation(
        text=f"<b>Total</b><br>{format_gp(total_profit)}",
        x=0.5, y=0.5,
        font=dict(color=_TEXT_YELLOW, size=12),
        showarrow=False
    )

    fig.update_layout(
        **_dark_layout(height=400, margin=dict(l=40, r=40, t=50, b=40)),
        title=dict(
            text="Profit by Category",
            font=dict(color=_TEXT_YELLOW, size=16)
        ),
        showlegend=False,
        uniformtext=dict(minsize=8, mode='hide'),
    )

    return fig


def create_profit_histogram(profits: List[float], per_item: bool = False) -> go.Figure:
    """Histogram of profit distribution."""
    profits_arr = np.array(profits)
    median_val = np.median(profits_arr)
    q1 = np.percentile(profits_arr, 25)
    q3 = np.percentile(profits_arr, 75)
    iqr = q3 - q1

    unit_label = "GP/item" if per_item else "GP"

    lower_fence = q1 - 3 * iqr
    upper_fence = q3 + 3 * iqr

    main_data = profits_arr[(profits_arr >= lower_fence) & (profits_arr <= upper_fence)]
    outliers = profits_arr[(profits_arr < lower_fence) | (profits_arr > upper_fence)]

    has_extreme_outliers = len(outliers) > 0 and len(main_data) >= len(profits_arr) * 0.75

    if has_extreme_outliers and len(main_data) > 0:
        hist_data = main_data
        outlier_note = f"{len(outliers)} extreme outlier(s) excluded"
    else:
        hist_data = profits_arr
        outlier_note = None

    profitable = hist_data[hist_data > 0]
    unprofitable = hist_data[hist_data <= 0]

    if len(hist_data) > 1:
        hist_min, hist_max = hist_data.min(), hist_data.max()
        hist_range = hist_max - hist_min
        target_bins = 20
        bin_size = hist_range / target_bins if hist_range > 0 else 1000

        if bin_size > 0:
            magnitude = 10 ** np.floor(np.log10(max(abs(bin_size), 1)))
            bin_size = np.ceil(bin_size / magnitude) * magnitude
        bin_size = max(bin_size, 100)
    else:
        bin_size = 10000

    fig = go.Figure()

    if len(profitable) > 0:
        fig.add_trace(
            go.Histogram(
                x=profitable,
                name=f'Profitable ({len(profitable)})',
                marker_color=_TEXT_ORANGE,
                marker_line_color='#b87333',
                marker_line_width=1,
                opacity=0.9,
                xbins=dict(size=bin_size),
                hovertemplate=f'<b>Profitable</b><br>Range: %{{x:,.0f}} {unit_label}<br>Count: %{{y}}<extra></extra>'
            )
        )

    if len(unprofitable) > 0:
        fig.add_trace(
            go.Histogram(
                x=unprofitable,
                name=f'Unprofitable ({len(unprofitable)})',
                marker_color=CHART_COLORS['dragon_red'],
                marker_line_color=CHART_COLORS['dragon_red_dark'],
                marker_line_width=1,
                opacity=0.9,
                xbins=dict(size=bin_size),
                hovertemplate=f'<b>Unprofitable</b><br>Range: %{{x:,.0f}} {unit_label}<br>Count: %{{y}}<extra></extra>'
            )
        )

    fig.add_vline(
        x=0,
        line_dash="solid",
        line_color="rgba(212,197,160,0.5)",
        line_width=2,
        annotation_text="Break-even",
        annotation_position="top",
        annotation_font=dict(color=_TEXT_LIGHT, size=10)
    )

    if not has_extreme_outliers or (lower_fence <= median_val <= upper_fence):
        fig.add_vline(
            x=median_val,
            line_dash="dot",
            line_color=CHART_COLORS['rune_blue'],
            line_width=2,
            annotation_text=f"Median: {format_gp(median_val)}",
            annotation_position="top right",
            annotation_font=dict(color='#5dade2', size=10)
        )

    subtitle_parts = [f"{len(hist_data)} chains"]
    if outlier_note:
        subtitle_parts.append(outlier_note)

    fig.update_layout(
        **_dark_layout(height=350),
        title=dict(
            text="Profit Distribution",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text=" - ".join(subtitle_parts),
                font=dict(color=_TEXT_GRAY, size=10)
            )
        ),
        xaxis=_dark_axis(f"Net Profit ({unit_label})", tickformat=',.0f',
                         zeroline=True, zerolinecolor='rgba(212,197,160,0.3)', zerolinewidth=1),
        yaxis=_dark_axis("Count"),
        bargap=0.05,
        barmode='overlay',
        legend=_dark_legend(),
    )

    return fig


def create_roi_scatter(results: List[Dict]) -> Optional[go.Figure]:
    """Scatter plot of ROI vs Profit. Returns None if insufficient data."""
    valid_results = [r for r in results if r.get("ROI %") is not None and r["ROI %"] != float('inf')]

    if len(valid_results) < 3:
        return None

    categories = {}
    for r in valid_results:
        cat = r.get("Category", "Unknown")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    fig = go.Figure()

    for cat, cat_results in categories.items():
        profits = [r["_profit_raw"] for r in cat_results]
        rois = [r["ROI %"] for r in cat_results]
        items = [get_clean_item_name(r["Item"]) for r in cat_results]

        color = CATEGORY_COLORS.get(cat, '#8e44ad')

        fig.add_trace(
            go.Scatter(
                x=profits,
                y=rois,
                mode='markers',
                name=cat,
                marker=dict(
                    size=10,
                    color=color,
                    line=dict(width=1, color=_BORDER_GOLD)
                ),
                text=items,
                hovertemplate='<b>%{text}</b><br>Category: ' + cat + '<br>Profit: %{x:,.0f} GP<br>ROI: %{y:.1f}%<extra></extra>'
            )
        )

    fig.add_hline(y=0, line_dash="dash", line_color="rgba(212,197,160,0.3)", line_width=1)
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(212,197,160,0.3)", line_width=1)

    fig.update_layout(
        **_dark_layout(height=400, margin=dict(l=55, r=20, t=60, b=80)),
        title=dict(
            text="ROI vs Profit",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text="Higher right = better value",
                font=dict(color=_TEXT_GRAY, size=10)
            )
        ),
        xaxis=_dark_axis("Net Profit (GP)", tickformat=',.0f'),
        yaxis=_dark_axis("ROI (%)"),
        legend=_dark_legend(),
    )

    return fig


def create_tier_category_heatmap(results: List[Dict]) -> Optional[go.Figure]:
    """
    Heatmap of profitability across material tiers (rows) × processing categories (cols).

    Each cell shows the per-item profit for that tier+category combo.
    Green = profitable, red = unprofitable, darker = larger magnitude.
    """
    from collections import defaultdict

    # Collect profit per (tier, category)
    grid: Dict[str, Dict[str, float]] = defaultdict(dict)
    for r in results:
        tier = get_tier_from_name(r["Item"])
        cat = r.get("Category", "Unknown")
        profit = r.get("_profit_raw", 0)
        grid[tier][cat] = profit

    if len(grid) < 2:
        return None

    # Ordered tier lists (low → high for both wood and metal)
    metal_order = ['Bronze', 'Iron', 'Steel', 'Black', 'Mithril', 'Adamant', 'Rune', 'Dragon']
    wood_order = ['Wooden', 'Oak', 'Teak', 'Mahogany', 'Camphor', 'Ironwood', 'Rosewood']

    present_metals = [t for t in metal_order if t in grid]
    present_woods = [t for t in wood_order if t in grid]
    other_tiers = [t for t in grid if t not in metal_order and t not in wood_order]

    # Rows: woods first, then metals (bottom to top in heatmap = reversed)
    tier_order = present_woods + present_metals + other_tiers

    # Columns: all categories present in the data
    all_cats = sorted({cat for tier_data in grid.values() for cat in tier_data})

    # Build the z-matrix, hover text, and annotation text
    z = []
    hover_text = []
    annot_text = []
    for tier in tier_order:
        row_z = []
        row_hover = []
        row_annot = []
        for cat in all_cats:
            val = grid[tier].get(cat)
            if val is not None:
                row_z.append(val)
                row_hover.append(f"<b>{tier} {cat}</b><br>Profit: {format_gp(val)}")
                row_annot.append(format_gp(val))
            else:
                row_z.append(None)
                row_hover.append(f"<b>{tier} {cat}</b><br>N/A")
                row_annot.append("")
        z.append(row_z)
        hover_text.append(row_hover)
        annot_text.append(row_annot)

    # Diverging colorscale: red → dark → green
    colorscale = [
        [0.0, '#c0392b'],    # deep red (worst loss)
        [0.35, '#5a2020'],   # dark red
        [0.5, '#2b2b2b'],    # neutral (break-even)
        [0.65, '#1a4a1a'],   # dark green
        [1.0, '#00ff00'],    # bright green (best profit)
    ]

    # Calculate symmetric zmax for balanced coloring
    flat_vals = [v for row in z for v in row if v is not None]
    if not flat_vals:
        return None
    abs_max = max(abs(v) for v in flat_vals) or 1

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=all_cats,
        y=tier_order,
        hovertext=hover_text,
        hoverinfo='text',
        text=annot_text,
        texttemplate='%{text}',
        textfont=dict(color=_TEXT_LIGHT, size=10),
        colorscale=colorscale,
        zmid=0,
        zmin=-abs_max,
        zmax=abs_max,
        colorbar=dict(
            title=dict(text='Profit (GP)', font=dict(color=_TEXT_ORANGE, size=10)),
            tickfont=dict(color=_TEXT_LIGHT, size=9),
            outlinecolor=_BORDER_GOLD,
            outlinewidth=1,
            bgcolor='rgba(43,43,43,0.8)',
        ),
        xgap=3,
        ygap=3,
    ))

    fig.update_layout(
        **_dark_layout(
            height=max(350, len(tier_order) * 45 + 120),
            margin=dict(l=100, r=30, t=60, b=80),
        ),
        title=dict(
            text="Tier × Category Profitability",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text="Green = profit, Red = loss",
                font=dict(color=_TEXT_GRAY, size=10),
            ),
        ),
        xaxis=_dark_axis("", tickangle=45, side='bottom'),
        yaxis=_dark_axis("", autorange='reversed'),
    )

    return fig


def create_cost_waterfall(result: Dict, item_name: str) -> go.Figure:
    """
    Waterfall chart showing cost breakdown for a single processing chain.

    Bars: Raw Materials → Processing → GE Tax → Output Value → Net Profit
    """
    raw_cost = result.get("raw_material_cost", 0)
    proc_cost = result.get("processing_costs", 0)
    ge_tax = result.get("ge_tax", 0)
    output_val = result.get("output_value", 0)
    net_profit = result.get("net_profit", 0)

    labels = ["Raw Materials", "Processing", "GE Tax", "Total Cost", "Output Value", "Net Profit"]
    values = [-raw_cost, -proc_cost, -ge_tax, 0, output_val, 0]
    measures = ["relative", "relative", "relative", "total", "absolute", "total"]

    # Colors per bar
    profit_color = '#00ff00' if net_profit >= 0 else '#c0392b'
    colors = {
        "increasing": _TEXT_ORANGE,
        "decreasing": '#c0392b',
        "totals": '#5dade2',
    }

    fig = go.Figure(go.Waterfall(
        name="Cost Breakdown",
        orientation="v",
        measure=measures,
        x=labels,
        y=values,
        text=[
            format_gp(raw_cost),
            format_gp(proc_cost),
            format_gp(ge_tax),
            format_gp(raw_cost + proc_cost + ge_tax),
            format_gp(output_val),
            format_gp(net_profit),
        ],
        textposition="outside",
        textfont=dict(color=_TEXT_YELLOW, size=10),
        connector=dict(
            line=dict(color=_BORDER_GOLD, width=1, dash="dot")
        ),
        increasing=dict(marker=dict(color=_TEXT_ORANGE, line=dict(color=_BORDER_GOLD, width=1))),
        decreasing=dict(marker=dict(color='#c0392b', line=dict(color=_BORDER_GOLD, width=1))),
        totals=dict(marker=dict(color='#5dade2', line=dict(color=_BORDER_GOLD, width=1))),
        hovertemplate='<b>%{x}</b><br>%{text}<extra></extra>',
    ))

    fig.update_layout(
        **_dark_layout(height=400, margin=dict(l=60, r=30, t=70, b=60)),
        title=dict(
            text=f"Cost Breakdown: {get_clean_item_name(item_name)}",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text=f"Net: {format_gp(net_profit)} ({'profit' if net_profit >= 0 else 'loss'})",
                font=dict(color=profit_color, size=11),
            ),
        ),
        xaxis=_dark_axis("", tickangle=30),
        yaxis=_dark_axis("GP", tickformat=',.0f'),
        showlegend=False,
        waterfallgap=0.3,
    )

    return fig


def create_multi_waterfall(results: List[Dict], top_n: int = 5) -> go.Figure:
    """
    Stacked waterfall comparison: shows cost structure for top N chains side by side.

    Each chain gets a group of bars: input cost (red), processing (orange), tax (gray),
    and output value (blue), with the net profit annotated.
    """
    sorted_results = sorted(results, key=lambda x: abs(x.get("_profit_raw", 0)), reverse=True)[:top_n]

    fig = go.Figure()

    items = [get_clean_item_name(r["Item"]) for r in sorted_results]
    raw_costs = [r.get("_raw_cost", 0) for r in sorted_results]
    proc_costs = [r.get("_proc_cost", 0) for r in sorted_results]
    taxes = [r.get("_tax", 0) for r in sorted_results]
    outputs = [r.get("_output", 0) for r in sorted_results]
    profits = [r.get("_profit_raw", 0) for r in sorted_results]

    # Stacked bars: costs negative, output positive
    fig.add_trace(go.Bar(
        name='Raw Materials',
        x=items,
        y=[-c for c in raw_costs],
        marker_color='#c0392b',
        marker_line_color=_BORDER_GOLD,
        marker_line_width=1,
        hovertemplate='<b>%{x}</b><br>Raw Materials: %{customdata}<extra></extra>',
        customdata=[format_gp(c) for c in raw_costs],
    ))

    fig.add_trace(go.Bar(
        name='Processing',
        x=items,
        y=[-c for c in proc_costs],
        marker_color=_TEXT_ORANGE,
        marker_line_color=_BORDER_GOLD,
        marker_line_width=1,
        hovertemplate='<b>%{x}</b><br>Processing: %{customdata}<extra></extra>',
        customdata=[format_gp(c) for c in proc_costs],
    ))

    fig.add_trace(go.Bar(
        name='GE Tax',
        x=items,
        y=[-t for t in taxes],
        marker_color=_TEXT_GRAY,
        marker_line_color=_BORDER_GOLD,
        marker_line_width=1,
        hovertemplate='<b>%{x}</b><br>Tax: %{customdata}<extra></extra>',
        customdata=[format_gp(t) for t in taxes],
    ))

    fig.add_trace(go.Bar(
        name='Output Value',
        x=items,
        y=outputs,
        marker_color=CHART_COLORS['rune_blue'],
        marker_line_color=_BORDER_GOLD,
        marker_line_width=1,
        hovertemplate='<b>%{x}</b><br>Output: %{customdata}<extra></extra>',
        customdata=[format_gp(o) for o in outputs],
    ))

    # Annotate net profit on each item
    for i, (item, profit) in enumerate(zip(items, profits)):
        color = '#00ff00' if profit >= 0 else '#c0392b'
        fig.add_annotation(
            x=item,
            y=outputs[i] + max(outputs) * 0.05,
            text=f"<b>{format_gp(profit)}</b>",
            showarrow=False,
            font=dict(color=color, size=10),
        )

    fig.update_layout(
        **_dark_layout(height=420, margin=dict(l=60, r=20, t=60, b=80)),
        title=dict(
            text="Cost Structure Comparison",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text=f"Top {len(sorted_results)} chains by absolute profit",
                font=dict(color=_TEXT_GRAY, size=10),
            ),
        ),
        xaxis=_dark_axis("", tickangle=30),
        yaxis=_dark_axis("GP", tickformat=',.0f',
                         zeroline=True, zerolinecolor='rgba(212,197,160,0.4)', zerolinewidth=1),
        barmode='relative',
        legend=_dark_legend(y=-0.30),
    )

    return fig


def create_category_comparison(results: List[Dict]) -> go.Figure:
    """Bar chart comparing categories by best/median/average profit."""
    category_data = {}

    for r in results:
        cat = r.get("Category", "Unknown")
        profit = r.get("_profit_raw", 0)

        if cat not in category_data:
            category_data[cat] = []
        category_data[cat].append(profit)

    categories = []
    bests = []
    medians = []
    averages = []

    for cat, profits in sorted(category_data.items(), key=lambda x: max(x[1]), reverse=True):
        categories.append(cat)
        bests.append(max(profits))
        medians.append(np.median(profits))
        averages.append(np.mean(profits))

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name='Best',
            x=categories,
            y=bests,
            marker_color=_TEXT_ORANGE,
            marker_line_color=_BORDER_GOLD,
            marker_line_width=1,
            text=[format_gp(v) for v in bests],
            textposition='outside',
            textfont=dict(size=9, color=_TEXT_YELLOW)
        )
    )

    fig.add_trace(
        go.Bar(
            name='Median',
            x=categories,
            y=medians,
            marker_color=CHART_COLORS['rune_blue'],
            marker_line_color=_BORDER_GOLD,
            marker_line_width=1,
            text=[format_gp(v) for v in medians],
            textposition='outside',
            textfont=dict(size=9, color=_TEXT_LIGHT)
        )
    )

    fig.add_trace(
        go.Bar(
            name='Average',
            x=categories,
            y=averages,
            marker_color='#8b7355',
            marker_line_color=_BORDER_GOLD,
            marker_line_width=1,
            text=[format_gp(v) for v in averages],
            textposition='outside',
            textfont=dict(size=9, color=_TEXT_LIGHT)
        )
    )

    fig.update_layout(
        **_dark_layout(height=400, margin=dict(l=55, r=20, t=60, b=100)),
        title=dict(
            text="Category Comparison",
            font=dict(color=_TEXT_YELLOW, size=16),
            subtitle=dict(
                text="Best, median, average profit per category",
                font=dict(color=_TEXT_GRAY, size=10)
            )
        ),
        xaxis=_dark_axis("", tickangle=45),
        yaxis=_dark_axis("Profit (GP)", tickformat=',.0f'),
        barmode='group',
        legend=_dark_legend(y=-0.35),
    )

    return fig
