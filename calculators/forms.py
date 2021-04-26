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
    
    def clean(self):
        """Override the clean method. cosolvent_fraction is required if a cosolvent is selected."""
        cleaned_data = super().clean()
        cosolvent = cleaned_data.get('cosolvent')
        cosolvent_fraction = cleaned_data.get('cosolvent_fraction')

        if cosolvent_fraction == None:
            if cosolvent == 'NONE':
                pass
            else:
                print('raise error')
                raise forms.ValidationError('You must specify the cosolvent fraction.')


class IsothermForm(forms.Form):
    ISOTHERMS = [
        ('linear', 'Linear'),
        ('langmuir', 'Langmuir'),
        ('linearlangmuir', 'Linear-Langmuir'),
        ('bilangmuir', 'Bi-Langmuir'),
        ('freundlich', 'Freundlich'),
    ]
    isotherm_type = forms.MultipleChoiceField(
        choices=ISOTHERMS, 
        label="Isotherm type", 
        widget=forms.CheckboxSelectMultiple()
    )
    xy_data = forms.CharField(
        label='XY Data', 
        widget=forms.Textarea(attrs={'rows': 12})
    )


class PCSAFTForm(forms.Form):
    COSOLVENTS = [
        ('NONE', 'No cosolvent'),
        ('ETHANOL', 'Ethanol'),
        ('WATER', 'Water'),
        ('METHANOL', 'Methanol'),
    ]
    cosolvent = forms.ChoiceField(
        choices=COSOLVENTS, 
        label="Cosolvent", 
        widget=forms.Select()
    )
    temperature = forms.FloatField(
        label='Temperature',
        min_value=-273.15,
        # widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    pressure = forms.FloatField(
        label='Pressure',
        min_value=0.001, 
    )
    cosolvent_fraction = forms.FloatField(
        label='Cosolvent fraction', 
        required=False,
        max_value=1, 
        min_value=0,
    )

    # Customize form widgets
    cosolvent.widget.attrs.update({'class': 'form-control'})
    temperature.widget.attrs.update({'class': 'form-control'})
    pressure.widget.attrs.update({'class': 'form-control'})
    cosolvent_fraction.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        """Override the clean method. cosolvent_fraction is required if a cosolvent is selected."""
        cleaned_data = super().clean()
        cosolvent = cleaned_data.get('cosolvent')
        cosolvent_fraction = cleaned_data.get('cosolvent_fraction')

        if cosolvent_fraction == None:
            if cosolvent == 'NONE':
                pass
            else:
                print('raise error')
                raise forms.ValidationError('You must specify the cosolvent fraction.')