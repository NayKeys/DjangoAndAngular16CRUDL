import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-student',
  templateUrl: './student.component.html',
  styleUrls: ['./student.component.css'],
})
export class StudentComponent implements OnInit {
  students: any[];
  displayDialog: boolean;
  student: any = {};
  selectedStudent: any;
  newStudent: boolean;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.refresh();
  }

  refresh() {
    this.http
      .post('http://localhost:8000/students_app/execute', {
        action: 'fetch_all',
      })
      .subscribe((response: any) => {
        this.students = response.students;
      });
  }

  showDialogToAdd() {
    this.newStudent = true;
    this.student = {};
    this.displayDialog = true;
  }

  save() {
    const students = [...this.students];
    if (this.newStudent) {
      this.http
        .post('http://localhost:8000/students_app/execute', {
          action: 'insert',
          data: { student: this.student },
        })
        .subscribe(() => {
          this.refresh();
        });
    } else {
      this.http
        .post('http://localhost:8000/students_app/execute', {
          action: 'update',
          data: { id: this.selectedStudent.id, student: this.student },
        })
        .subscribe(() => {
          this.refresh();
        });
    }
    this.student = null;
    this.displayDialog = false;
  }

  delete() {
    this.http
      .post('http://localhost:8000/students_app/execute', {
        action: 'delete',
        data: { id: this.selectedStudent.id },
      })
      .subscribe(() => {
        this.refresh();
      });
    this.displayDialog = false;
  }

  onRowSelect(event) {
    this.newStudent = false;
    this.student = this.cloneStudent(event.data);
    this.displayDialog = true;
  }

  cloneStudent(s: any): any {
    const student = {};
    for (const prop in s) {
      student[prop] = s[prop];
    }
    return student;
  }
}
