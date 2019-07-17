from django import forms


class CarbonDioxideForm(forms.Form):
    COSOLVENTS = [
        ('NONE', 'No cosolvent'),
        ('ETHANOL', 'Ethanol'),
    ]
    cosolvent = forms.ChoiceField(
        choices=COSOLVENTS, 
        label="Cosolvent", 
        widget=forms.Select()
    )
    temperature = forms.FloatField(
        label='Temperature in Celsius',
        # widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    pressure = forms.FloatField(
        label='Pressure in bar'
    )
    cosolvent_fraction = forms.FloatField(
        label='Cosolvent mass fraction', 
        required=False,
        max_value=1, 
        min_value=0,
    )
    