"use strict";
exports.__esModule = true;
var testing_1 = require("@angular/core/testing");
var textbox_comp_component_1 = require("./textbox-comp.component");
describe('TextboxCOMPComponent', function () {
    var component;
    var fixture;
    beforeEach(testing_1.async(function () {
        testing_1.TestBed.configureTestingModule({
            declarations: [textbox_comp_component_1.TextboxCOMPComponent]
        })
            .compileComponents();
    }));
    beforeEach(function () {
        fixture = testing_1.TestBed.createComponent(textbox_comp_component_1.TextboxCOMPComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });
    it('should create', function () {
        expect(component).toBeTruthy();
    });
});
