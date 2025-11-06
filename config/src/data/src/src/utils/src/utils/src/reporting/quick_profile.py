from pathlib import Path
import pandas as pd

def dataframe_profile_md(df: pd.DataFrame, title: str = "Dataset Profile") -> str:
    lines = [f"# {title}", ""]
    lines.append(f"- Rows: **{len(df)}**")
    lines.append(f"- Columns: **{len(df.columns)}**")
    lines.append("")
    lines.append("## Columns & Dtypes")
    lines.append("")
    for c in df.columns:
        lines.append(f"- `{c}`: `{df[c].dtype}` (nulls: {int(df[c].isna().sum())})")
    lines.append("")
    lines.append("## Numeric Summary")
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        desc = df[num_cols].describe().T
        lines.append(desc.to_markdown())
        lines.append("")
    lines.append("## Sample Rows")
    lines.append(df.head(10).to_markdown(index=False))
    lines.append("")
    return "\n".join(lines)

def write_profile_md(df: pd.DataFrame, out_path: str, title: str = "Dataset Profile") -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    content = dataframe_profile_md(df, title)
    Path(out_path).write_text(content, encoding="utf-8")
    return out_path
