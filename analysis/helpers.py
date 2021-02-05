def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height().round(1)
        ax.annotate('{}%'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', 
                    color="black", size=6.5)


def autolabel_count(rects, ax, df):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect, (i, rows) in zip(rects, df.iterrows()):
        low_lb = "("+str(int(rows["total"]))+")"

        ax.annotate(
            '{}'.format(low_lb),
            xy=(rect.get_x() + rect.get_width() / 2, 2),
            xytext=(0, 0),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom', 
            color="black", size=6.5)


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct
    

def autolabel_count_boxed(rects, ax, df):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect, (i, rows) in zip(rects, df.iterrows()):
        low_lb = "("+str(int(rows["total"]))+")"

        ax.annotate(
            '{}'.format(low_lb),
            xy=(rect.get_x() + rect.get_width() / 2, 2),
            xytext=(0, 0),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom', 
            color="black", size=6.5,
            bbox=dict(facecolor='white', boxstyle='round', alpha=0.80, pad=0.01))


def fix_name(el):
    return el.split('Dataverse')[0].strip()


def fix_name2(x):
    if 'International Interactions (II)' in x:
        return 'International Interactions (II)'
    if 'American Journal of Political Science (AJPS)' in x:
        return 'American Journal of Political\nScience (AJPS)'
    if 'British Journal of Political Science' in x:
        return 'British Journal of\nPolitical Science'
    if 'American Political Science Review' in x:
        return 'American Political\nScience Review'
    if 'Review of Economics and Statistics' in x:
        return 'Review of Economics\nand Statistics'
    if 'Political Science Research and Methods (PSRM)' in x:
        return 'Political Science Research\nand Methods (PSRM)'
    if 'Journal of Experimental Political Science' in x:
        return 'Journal of Experimental\nPolitical Science'
    if 'International Studies Quarterly' in x:
        return 'International\nStudies Quarterly'
    return x