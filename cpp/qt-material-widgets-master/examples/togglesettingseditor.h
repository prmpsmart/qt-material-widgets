#ifndef TOGGLESETTINGSEDITOR_H
#define TOGGLESETTINGSEDITOR_H

#include <QWidget>
#include "ui_togglesettingsform.h"

class QtMaterialToggle;

class ToggleSettingsEditor : public QWidget
{
    Q_OBJECT

public:
    explicit ToggleSettingsEditor(QWidget *parent = 0);
    ~ToggleSettingsEditor();

protected slots:
    void setupForm();
    void updateWidget();
    void selectColor();

private:
    Ui::ToggleSettingsForm *const ui;
    QtMaterialToggle       *const m_toggle;
};

#endif // TOGGLESETTINGSEDITOR_H
