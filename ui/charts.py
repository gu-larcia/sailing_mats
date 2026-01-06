"""
Plotly chart functions for profit analytics.

All charts use the OSRS-authentic color scheme and are optimized for
both desktop and mobile viewing.
"""

from typing import Dict, List, Optional
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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


def create_profit_chart(results: List[Dict], top_n: int = 10) -> go.Figure:
    """
    Create a horizontal bar chart of top profitable chains.
    
    Args:
        results: List of chain result dicts with '_profit_raw', 'Item', 'Category'
        top_n: Number of top results to show
        
    Returns:
        Plotly Figure
    """
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
            marker_line_color='#1a2a3a',
            marker_line_width=1.5,
            text=[format_gp(p) for p in profits],
            textposition='outside',
            textfont=dict(color='#f4e4bc', size=10),
            name='Profit',
            customdata=list(zip(categories, tiers)),
            hovertemplate='<b>%{y}</b><br>Category: %{customdata[0]}<br>Tier: %{customdata[1]}<br>Profit: %{x:,.0f} GP<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Top Profitable Chains",
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text=f"Top {len(sorted_results)} by profit - colored by tier",
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title="Net Profit (GP)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f'
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color='#f4e4bc', size=9),
            autorange="reversed"
        ),
        height=max(380, top_n * 36),
        margin=dict(l=140, r=80, t=60, b=45),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False
    )
    
    return fig


def create_category_pie(results: List[Dict]) -> go.Figure:
    """
    Create a pie chart showing profit distribution by category.
    
    Args:
        results: List of chain result dicts
        
    Returns:
        Plotly Figure
    """
    category_profits = {}
    category_counts = {}
    
    for r in results:
        cat = r.get("Category", "Unknown")
        profit = max(0, r.get("_profit_raw", 0))
        category_profits[cat] = category_profits.get(cat, 0) + profit
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    sorted_cats = sorted(category_profits.items(), key=lambda x: x[1], reverse=True)
    total_profit = sum(category_profits.values())
    
    # Group small categories into "Other"
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
            textfont=dict(color='#f4e4bc', size=10),
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(
                colors=colors,
                line=dict(color='#1a2a3a', width=2)
            ),
            pull=[0.03 if i == 0 else 0 for i in range(len(labels))],
            insidetextorientation='horizontal',
            sort=False
        )
    ])
    
    fig.add_annotation(
        text=f"<b>Total</b><br>{format_gp(total_profit)}",
        x=0.5, y=0.5,
        font=dict(color='#ffd700', size=12),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text="Profit by Category",
            font=dict(color='#ffd700', size=16)
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        uniformtext=dict(minsize=8, mode='hide')
    )
    
    return fig


def create_profit_histogram(profits: List[float], per_item: bool = False) -> go.Figure:
    """
    Create a histogram showing profit distribution.
    
    Args:
        profits: List of profit values
        per_item: Whether values are per-item (affects labels)
        
    Returns:
        Plotly Figure
    """
    profits_arr = np.array(profits)
    median_val = np.median(profits_arr)
    q1 = np.percentile(profits_arr, 25)
    q3 = np.percentile(profits_arr, 75)
    iqr = q3 - q1
    
    unit_label = "GP/item" if per_item else "GP"
    
    # Exclude extreme outliers (beyond 3x IQR)
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
    
    # Separate profitable and unprofitable
    profitable = hist_data[hist_data > 0]
    unprofitable = hist_data[hist_data <= 0]
    
    # Calculate bin size
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
                marker_color=CHART_COLORS['gold'],
                marker_line_color=CHART_COLORS['gold_dark'],
                marker_line_width=1,
                opacity=0.9,
                xbins=dict(size=bin_size),
                hovertemplate=f'<b>Profitable Chains</b><br>Range: %{{x:,.0f}} {unit_label}<br>Count: %{{y}}<extra></extra>'
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
                hovertemplate=f'<b>Unprofitable Chains</b><br>Range: %{{x:,.0f}} {unit_label}<br>Count: %{{y}}<extra></extra>'
            )
        )
    
    # Add break-even line
    fig.add_vline(
        x=0, 
        line_dash="solid", 
        line_color="rgba(244,228,188,0.5)",
        line_width=2,
        annotation_text="Break-even",
        annotation_position="top",
        annotation_font=dict(color='#f4e4bc', size=10)
    )
    
    # Add median line
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
    
    title_text = "Profit Distribution"
    subtitle_parts = [f"Showing {len(hist_data)} chains"]
    if outlier_note:
        subtitle_parts.append(outlier_note)
    subtitle_text = " - ".join(subtitle_parts)
    
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text=subtitle_text,
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title=f"Net Profit ({unit_label})",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f',
            zeroline=True,
            zerolinecolor='rgba(244,228,188,0.3)',
            zerolinewidth=1
        ),
        yaxis=dict(
            title="Count",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)'
        ),
        height=350,
        margin=dict(l=55, r=20, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        bargap=0.05,
        barmode='overlay',
        legend=dict(
            font=dict(color='#f4e4bc', size=10),
            bgcolor='rgba(26,42,58,0.8)',
            bordercolor='#8b7355',
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5
        )
    )
    
    return fig


def create_roi_scatter(results: List[Dict]) -> Optional[go.Figure]:
    """
    Create a scatter plot of ROI vs Profit.
    
    Args:
        results: List of chain result dicts
        
    Returns:
        Plotly Figure, or None if insufficient data
    """
    # Filter results with valid ROI
    valid_results = [r for r in results if r.get("ROI %") is not None and r["ROI %"] != float('inf')]
    
    if len(valid_results) < 3:
        return None
    
    # Group by category
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
                    line=dict(width=1, color='#1a2a3a')
                ),
                text=items,
                hovertemplate='<b>%{text}</b><br>Category: ' + cat + '<br>Profit: %{x:,.0f} GP<br>ROI: %{y:.1f}%<extra></extra>'
            )
        )
    
    # Add reference lines
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(244,228,188,0.3)", line_width=1)
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(244,228,188,0.3)", line_width=1)
    
    fig.update_layout(
        title=dict(
            text="ROI vs Profit Analysis",
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text="Higher right = better overall value",
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title="Net Profit (GP)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f'
        ),
        yaxis=dict(
            title="ROI (%)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)'
        ),
        height=400,
        margin=dict(l=55, r=20, t=60, b=80),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        legend=dict(
            font=dict(color='#f4e4bc', size=10),
            bgcolor='rgba(26,42,58,0.8)',
            bordercolor='#8b7355',
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5
        )
    )
    
    return fig


def create_category_comparison(results: List[Dict]) -> go.Figure:
    """
    Create a bar chart comparing categories by best/median/average profit.
    
    Args:
        results: List of chain result dicts
        
    Returns:
        Plotly Figure
    """
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
            marker_color=CHART_COLORS['gold'],
            text=[format_gp(v) for v in bests],
            textposition='outside',
            textfont=dict(size=9, color='#f4e4bc')
        )
    )
    
    fig.add_trace(
        go.Bar(
            name='Median',
            x=categories,
            y=medians,
            marker_color=CHART_COLORS['rune_blue'],
            text=[format_gp(v) for v in medians],
            textposition='outside',
            textfont=dict(size=9, color='#f4e4bc')
        )
    )
    
    fig.add_trace(
        go.Bar(
            name='Average',
            x=categories,
            y=averages,
            marker_color=CHART_COLORS['driftwood'],
            text=[format_gp(v) for v in averages],
            textposition='outside',
            textfont=dict(size=9, color='#f4e4bc')
        )
    )
    
    fig.update_layout(
        title=dict(
            text="Category Comparison",
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text="Best, Median, and Average profit per category",
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title="",
            tickfont=dict(color='#f4e4bc', size=9),
            tickangle=45
        ),
        yaxis=dict(
            title="Profit (GP)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f'
        ),
        height=400,
        margin=dict(l=55, r=20, t=60, b=100),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        barmode='group',
        legend=dict(
            font=dict(color='#f4e4bc', size=10),
            bgcolor='rgba(26,42,58,0.8)',
            bordercolor='#8b7355',
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=-0.35,
            xanchor='center',
            x=0.5
        )
    )
    
    return fig
