from flask import render_template, flash, redirect, session, request
from app import app, db, models
from .forms import AssessmentForm
from .models import Assessment

#default/index page -> all assessments
#Displays all assessments, if none then appropriate message should be shown instead
#Displays 2 sets - in progress and complete. Also includes 2 buttons on each - to complete/unfinish or delete
@app.route('/')
def AllAssessments():
    assessments = Assessment.query.all()
    return render_template('allassessments.html',
                           title="Homepage",
                           assessments=assessments) 

#2nd page -> new assessment
#Allow user to enter details to add a new assignment, uses a form and validates inputs before submission
@app.route('/newassessment', methods=['GET', 'POST'])
def NewAssessment():
    session.pop('_flashes', None)
    form = AssessmentForm()
    if form.validate_on_submit():
        new_assessment = Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            deadline=form.deadline.data,
            description=form.description.data,
            is_completed=form.is_completed.data)
        db.session.add(new_assessment)
        db.session.commit()
        flash("Assessment added to database successfully")
    return render_template('newassessment.html',
                           title="Add New Assessment",
                           form=form,)

#3rd page -> current assessments
#Show user all assessments that are current e.g. is_completed = false. User can also edit info or delete any of these assessments
@app.route('/currentassessments')
def CurrentAssessments():
    assessments = Assessment.query.filter_by(is_completed=False).all()
    return render_template('currentassessments.html',
                           title="Current Assessments",
                           assessments=assessments)

#4th page -> complete assessments
#Show user all assessments that are complete e.g. is_completed = true. User can also edit info or delete any of these assessments
@app.route('/completeassessments')
def CompleteAssessments():
    assessments = Assessment.query.filter_by(is_completed=True).all()
    return render_template('completeassessments.html',
                           title="Complete Assessments",
                           assessments=assessments)

#5th page -> edit assignment
#will take a selected assignment and have a form for the user to edit it
@app.route('/editassessment/<int:assessment_id>', methods=['GET', 'POST'])
def EditAssessment(assessment_id):
    #get the assessment by ID
    assessment = Assessment.query.get(assessment_id)    
    form = AssessmentForm(obj=assessment)
    if form.validate_on_submit():
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline = form.deadline.data
        assessment.description = form.description.data
        assessment.is_completed = form.is_completed.data
        db.session.commit()
        flash('Assessment updated successfully!')
    return render_template('editassessment.html',
                            title="Edit Assignment", 
                            form=form, 
                            assessment=assessment)

#Route for POST request to delete a record of an assignment in the database
@app.route('/deleteassessment/<int:assessment_id>', methods=['POST']) 
def DeleteAssessment(assessment_id):
    assessment = Assessment.query.get(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!')
    return redirect(request.referrer)

#Route for POST request to mark a record of an assignment in the database as complete
@app.route('/complete_assessment/<int:assessment_id>', methods=['POST'])
def CompleteAssessment(assessment_id):
    assessment = Assessment.query.get(assessment_id)
    assessment.is_completed = True
    db.session.commit()
    flash('Assessment marked as Complete!')
    return redirect(request.referrer)

#Route for POST request to mark a record of an assignment in the database as incomplete
@app.route('/uncomplete_assessment/<int:assessment_id>', methods=['POST'])
def UncompleteAssessment(assessment_id):
    assessment = Assessment.query.get(assessment_id)
    assessment.is_completed = False
    db.session.commit()
    flash('Assessment marked as Uncomplete!')
    return redirect(request.referrer)