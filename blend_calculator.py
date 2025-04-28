import pandas as pd

class BlendCalculator:
    """
    Classe para calcular parâmetros físico-químicos do Blend LG
    usando o arquivo Excel gerado (Blend_LG_Modelagem.xlsx).
    """

    def __init__(self, excel_path: str):
        # Carrega perfis de óleos do Excel
        self.profiles = pd.read_excel(excel_path, sheet_name='Perfis_Oleos')
        # Ajusta nomes das colunas
        self.profiles.columns = [
            'Oil', 'Iodine', 'Saponification', 'MeltingPoint'
        ]

    def compute(self, blend_percentages: dict) -> dict:
        """
        Calcula II, IS e PF do blend
        blend_percentages: { 'Palm Oil': 50, ... }
        Retorna dicionário com resultados.
        """
        df = self.profiles.copy()
        df['Perc'] = df['Oil'].map(blend_percentages).fillna(0)
        df['II_contrib'] = df['Iodine'] * df['Perc'] / 100
        df['IS_contrib'] = df['Saponification'] * df['Perc'] / 100
        df['PF_contrib'] = df['MeltingPoint'] * df['Perc'] / 100

        II = df['II_contrib'].sum()
        IS = df['IS_contrib'].sum()
        PF = df['PF_contrib'].sum()

        return {
            'Índice de Iodo (II)': II,
            'Índice de Saponificação (IS)': IS,
            'Ponto de Fusão (PF)': PF
        }

# Exemplo de uso
if __name__ == '__main__':
    calc = BlendCalculator('Blend_LG_Modelagem.xlsx')
    meu_blend = {
        'Palm Oil': 40,
        'Palm Olein': 10,
        'Palm Stearin': 10,
        'Palm Kernel Oil': 30,
        'Palm Kernel Olein': 5,
        'Palm Kernel Stearin': 5
    }
    resultados = calc.compute(meu_blend)
    print("Resultados do Blend LG:", resultados)
