from django import forms
from .models import CharacterNote

class CharacterNoteForm(forms.ModelForm):
    class Meta:
        model = CharacterNote
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a note...'}),
        }
