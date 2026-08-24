#!/usr/bin/env python3

import pandas as pd

def growing_municipalities(df):
    pass

def main():
    df = pd.read_csv('src/municipal.tsv', sep='\t', index_col=0)
    df = df["Akaa":"Äänekoski"]
    dec = growing_municipalities(df)
    print(f"Proportion of growing municipalities: {dec:.1f}%")


if __name__ == "__main__":
    main()
