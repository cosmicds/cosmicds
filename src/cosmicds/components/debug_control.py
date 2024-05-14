import solara
from solara import Reactive
import reacton.ipyvuetify as rv

from dataclasses import fields

from functools import partial

@solara.component
def MarkerSelector(markers, current_step):
    
    markers_list = [marker.name for marker in markers]
        
    with solara.Row():
        with solara.Column():   
            rv.Select(
                label="Select Marker", 
                v_model=current_step.value.name, 
                on_v_model=lambda value: current_step.set(markers[value]), 
                items=markers_list
            )


@solara.component
def FieldList(component_state):
    print(component_state)
    field_names = [{'name':f.name, 'type':f.type, 'attr': getattr(component_state, f.name, Reactive)} for f in fields(component_state)]
            
    for field in field_names:
        field_attr = field['attr']
        field_type = field['type']
        if field['name'] == "current_step":
            continue
        elif field_type == Reactive[bool]:
            rv.Switch(label=field['name'], v_model=field_attr.value, on_v_model=partial(field_attr.set))
        elif field_type == Reactive[str]:
            solara.InputText(label=field['name'], value=field_attr)
        elif field_type == Reactive[int]:
            solara.InputInt(label=field['name'], value=field_attr)
        elif field_type == Reactive[float]:
            solara.InputFloat(label=field['name'], value=field_attr)
        else:
            # just print it out
            solara.Markdown(f"{field['name']}: {field_attr.value}")


@solara.component
def StateEditor(markers, component_state):
    show_dialog, set_show_dialog = solara.use_state(False)
    with solara.Row():
        MarkerSelector(markers, getattr(component_state, 'current_step', Reactive))
        solara.Button(
            children="Edit State",
            on_click=lambda: set_show_dialog(not show_dialog)
        )
        solara.Markdown(f"{show_dialog}")
        with rv.Dialog(v_model=show_dialog, on_v_model=set_show_dialog, max_width="500px"):
            with solara.Card():
                with solara.Column():
                    FieldList(component_state)