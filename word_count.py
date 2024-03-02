"""Taller evaluable"""

import glob
import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    filenames = glob.glob(f"{input_directory}/*.txt")
    dataframes = [
        pd.read_csv(filename, sep="\t", header=None, names=["text"])
        for filename in filenames
    ] # list comprehension

    concatenated_df = pd.concat(dataframes, ignore_index=True) #No reinicia el conteo en cada dataFrame
    return concatenated_df


def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    df = dataframe.copy()
    df["text"] = df["text"].str.lower()
    df["text"] = df["text"].str.replace(".","")
    df["text"] = df["text"].str.replace(",","")
    return df

def count_words(dataframe):
    """Word count"""
    df = dataframe.copy()
    df["text"] = df["text"].str.split()
    df = df.explode("text")
    df = df["text"].value_counts()
    #   df = df.groupby("text", as_index=False).agg({"count":"sum"})
    return df

def count_words_(dataframe):
    """Word count"""
    df = dataframe.copy()
    df["text"] = df["text"].str.split()
    df = df.explode("text")
    df["count"] = 1
    df = df.groupby("text").agg({"count":"sum"})
    #   df = df.groupby("text", as_index=False).agg({"count":"sum"})
    return df


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, sep="\t", index=True, header=False)



#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    df = load_input(input_directory)
    df = clean_text(df)
    df = count_words(df)
    save_output(df,output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
