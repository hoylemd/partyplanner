import FormComponent from './FormComponent';

class EventForm extends FormComponent {
  fields = {
    name: {type: 'text', label: 'Name'},
    description: {type: 'textarea', label: 'Description'},
    starts_at: {type: 'date', label: 'Starts at'},
    ends_at: {type: 'date', label: 'Ends at'},
    image: {type: 'text', label: 'Image'}
  }

}
EventForm.propTypes = {
  ...FormComponent.propTypes,
};

export default EventForm;
