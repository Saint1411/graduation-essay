package ca.pfv.spmf.gui;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import java.awt.TextArea;
import java.awt.Dialog.ModalityType;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class AboutWindow extends JDialog{
	public AboutWindow(JFrame window) {
		super(window);
		
		setResizable(false);
		setTitle("About SPMF");
		getContentPane().setLayout(null);
		
		// set this window as visible
		setVisible(true);
		// show this window as modal
		setModal(true);
		setModalityType(ModalityType.APPLICATION_MODAL);
		
		JLabel lblNewLabel = new JLabel("");
		lblNewLabel.setIcon(new ImageIcon(AboutWindow.class.getResource("/ca/pfv/spmf/gui/spmf.png")));
		lblNewLabel.setBounds(221, 11, 210, 51);
		getContentPane().add(lblNewLabel);
		
		JButton btnNewButton = new JButton("Close");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				// hide this window
				setVisible(false);
			}
		});
		btnNewButton.setBounds(283, 262, 89, 23);
		getContentPane().add(btnNewButton);
		
		TextArea textArea = new TextArea();
		textArea.setText(
				"Thanks for using SPMF!" + System.lineSeparator() + System.lineSeparator() +
				"SPMF is distributed under the open-source GNU GPL license version 3." +  System.lineSeparator() + "This license is available at: <http://www.gnu.org/licenses/>." + System.lineSeparator() + System.lineSeparator() +
				"SPMF was founded in 2008 by Philippe Fournier-Viger and many persons have contributed to the project." + System.lineSeparator() + System.lineSeparator() + 
				"Click the buttons below for more information:");
		textArea.setEditable(false);
		textArea.setRows(10);
		textArea.setBounds(10, 68, 629, 149);
		getContentPane().add(textArea);
		
		// Set the window as modal
		setModalExclusionType(ModalExclusionType.APPLICATION_EXCLUDE);
		
		JButton btnNewButton_1 = new JButton("Documentation");
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				openWebPage("http://philippe-fournier-viger.com/spmf/index.php?link=documentation.php");
			}
		});
		btnNewButton_1.setBounds(402, 223, 133, 23);
		getContentPane().add(btnNewButton_1);
		
		JButton btnNewButton_2 = new JButton("Contributors");
		btnNewButton_2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				openWebPage("http://philippe-fournier-viger.com/spmf/index.php?link=contributors.php");
			}
		});
		btnNewButton_2.setBounds(267, 223, 125, 23);
		getContentPane().add(btnNewButton_2);
		
		JButton btnNewButton_3 = new JButton("Website");
		btnNewButton_3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				openWebPage("http://www.philippe-fournier-viger.com/spmf/");
			}
		});
		btnNewButton_3.setBounds(131, 223, 126, 23);
		getContentPane().add(btnNewButton_3);
		
		setSize(680,350);
		// set this window as visible
		setVisible(true);
		// show this window as modal
		setModal(true);
		setModalityType(ModalityType.APPLICATION_MODAL);
	}
	
	/**
	 * This method open a URL in the default web browser.
	 *
	 * @param url : URL of the webpage
	 */
	private void openWebPage(String url) {
		try {
			java.awt.Desktop.getDesktop().browse(java.net.URI.create(url));
		} catch (java.io.IOException e) {
			System.out.println(e.getMessage());
		}
	} 
}
