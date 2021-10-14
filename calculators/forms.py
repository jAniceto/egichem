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
        # ('WATER', 'Water'),
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
    cosolvent_fraction.widget.attrs.update({'class': 'form-control', 'step': '0.01'})

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


class GeneralPCSAFTForm(forms.Form):
    temperature = forms.FloatField(
        label='Temperature', 
        required=False,
    )
    pressure = forms.FloatField(
        label='Pressure', 
        required=False,
        min_value=0.001, 
    )
    # Component 1
    molar_fraction_1 = forms.FloatField(
        label='Component 1 molar fraction', 
        required=False,
        max_value=1, 
        min_value=0,
    )
    molar_mass_1 = forms.FloatField(
        label='Component 1 molar mass', 
        required=False,
        min_value=0,
    )
    m_1 = forms.FloatField(
        label='Component 1 segment number', 
        required=False,
    )
    s_1 = forms.FloatField(
        label='Component 1 segment diameter', 
        required=False,
    )
    e_1 = forms.FloatField(
        label='Component 1 dispersion energy', 
        required=False,
    )
    vol_assoc_1 = forms.FloatField(
        label='Component 1 association volume',
    )
    e_assoc_1 = forms.FloatField(
        label='Component 1 association energy',
    )
    # Component 2
    molar_mass_2 = forms.FloatField(
        label='Component 1 molar mass', 
        required=False,
        min_value=0,
    )
    m_2 = forms.FloatField(
        label='Component 2 segment number', 
        required=False,
    )
    s_2 = forms.FloatField(
        label='Component 2 segment diameter', 
        required=False,
    )
    e_2 = forms.FloatField(
        label='Component 2 dispersion energy', 
        required=False,
    )
    vol_assoc_2 = forms.FloatField(
        label='Component 2 association volume',
        required=False,
    )
    e_assoc_2 = forms.FloatField(
        label='Component 2 association energy',
        required=False,
    )
    # Interaction parameters
    k_12 = forms.FloatField(
        label='Binary interaction parameters',
        required=False,
    )

    # Customize form widgets
    temperature.widget.attrs.update({'class': 'form-control'})
    pressure.widget.attrs.update({'class': 'form-control'})
    molar_fraction_1.widget.attrs.update({'class': 'form-control', 'id': 'molarFractionComponent1', 'placeholder': 'Comp 1'})
    molar_mass_1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1'})
    molar_mass_2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 2'})
    m_1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1'})
    m_2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 2'})
    s_1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1'})
    s_2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 2'})
    e_1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1'})
    e_2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 2'})
    vol_assoc_1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1'})
    vol_assoc_2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 2'})
    e_assoc_1.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1'})
    e_assoc_2.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 2'})
    k_12.widget.attrs.update({'class': 'form-control', 'placeholder': 'Comp 1 - Comp 2'})


class KlinkenbergForm(forms.Form):
    equilibrium_constant = forms.FloatField(
        label='Equilibrium constant', 
        required=True,
        min_value=0,
    )
    kinetic_constant = forms.FloatField(
        label='Kinetic constant', 
        required=True,
        min_value=0,
    )
    feed_concentration = forms.FloatField(
        label='Feed concentration', 
        required=True,
        min_value=0,
    )
    length = forms.FloatField(
        label='Column length', 
        required=True,
        min_value=0,
    )
    porosity = forms.FloatField(
        label='Bulk porosity', 
        required=True,
        min_value=0,
    )
    velocity = forms.FloatField(
        label='Interstitial velocity', 
        required=True,
        min_value=0,
    )
    time_final = forms.FloatField(
        label='Final time', 
        required=True,
        min_value=0,
    )
    xy_data = forms.CharField(
        label='Experimental data', 
        required=False,
        widget=forms.Textarea(attrs={'rows': 16})
    )
    # Customize form widgets
    equilibrium_constant.widget.attrs.update({'class': 'form-control'})
    kinetic_constant.widget.attrs.update({'class': 'form-control'})
    feed_concentration.widget.attrs.update({'class': 'form-control'})
    length.widget.attrs.update({'class': 'form-control'})
    porosity.widget.attrs.update({'class': 'form-control'})
    velocity.widget.attrs.update({'class': 'form-control'})
    time_final.widget.attrs.update({'class': 'form-control'})
    xy_data.widget.attrs.update({'class': 'form-control'})